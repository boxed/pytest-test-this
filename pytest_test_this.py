import re
from collections import defaultdict
from functools import lru_cache
from subprocess import check_output
from typing import DefaultDict, Set

from _pytest.nodes import Node


def pytest_addoption(parser):
    group = parser.getgroup("test_this")
    group.addoption(
        "--test-this",
        action="store",
        dest="test_this",
        help='Name of thing to find tests for',
    )
    group.addoption(
        "--test-this-git",
        action="store_true",
        dest="test_this_git",
        help='Try to figure out what to test based on a git diff',
    )


skip_all = False


@lru_cache(1)
def get_symbols_from_config(config):
    if config.getoption('test_this_git', default=None):
        diff = check_output(['git', 'diff']).decode().split('\n')

        changed_functions = {
            x.rpartition('@@')[-1].partition('(')[0].replace('def ', '').replace('class ', '')
            for x in diff if x.startswith('@@')
        }

        if not changed_functions:
            global skip_all
            skip_all = True

        return changed_functions

    symbols = config.getoption('test_this', default=None)
    if symbols is None:
        return None

    return {x for x in set(symbols.split(',')) if x}


def pytest_collection_modifyitems(config, items):
    if skip_all:
        items[:] = []

    symbols = get_symbols_from_config(config)
    if not symbols:
        return

    files = {x.fspath for x in items}

    results = defaultdict(set)
    for path in files:
        f = LazyFileContents(path)
        find_for_file(
            f=f,
            full_path=path,
            results=results,
            symbols=symbols,
        )

    def keep(node: Node):
        if node.fspath not in results:
            return False
        test_name_excluding_parameters = node.name.partition('[')[0]
        if test_name_excluding_parameters in results[node.fspath]:
            return True
        return False

    items[:] = [node for node in items if keep(node)]


def pytest_ignore_collect(path, config):
    if not path.strpath.endswith('.py'):
        return

    symbols = get_symbols_from_config(config)
    if not symbols:
        return

    f = LazyFileContents(path)

    # let's just do the quick check here
    if all(symbol not in f.contents for symbol in symbols):
        return True


def check_line(*, i: int, line: str, symbols: Set[str], full_path, f, results: DefaultDict[str, set]):
    symbols_joined = '|'.join(symbols)
    if re.search(rf'\b({symbols_joined})\b', line):
        if not line.startswith(' '):
            return

        # find the first previously non-indented line
        found_test_line = None
        for l in reversed(f.lines[:i]):
            if l.startswith('def test_'):
                found_test_line = l
                break

            # we found a non-indented block, but it wasn't a test definition, so ignore this line
            if not l.startswith(' ') and not l.startswith('\t'):
                continue

        if found_test_line is None:
            return

        test_name = re.match(r'def (test_.+)\(', found_test_line).groups()[0]
        results[full_path].add(test_name)


def find_for_file(*, f, full_path, results: DefaultDict[str, set], symbols: Set[str]):
    if any(symbol in f.contents for symbol in symbols):
        for i, line in enumerate(f.lines):
            check_line(
                i=i,
                line=line,
                symbols=symbols,
                full_path=full_path,
                f=f,
                results=results,
            )


dir_whitelist = {
    '__pycache__',
    'venv',
    'dependencies',
    'node_modules',
    'docker',
    'htmlcov',
}

filename_whitelist = {
    __file__.split('/')[-1],
}


class LazyFileContents:
    def __init__(self, full_path):
        self.full_path = full_path
        self._contents = None
        self._lines = None

    @property
    def contents(self):
        if self._contents is None:
            self._contents = open(self.full_path, encoding='utf8').read()

        return self._contents

    @property
    def lines(self):
        if self._lines is None:
            self._lines = self.contents.split('\n')
        return self._lines
