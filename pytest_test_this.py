import re
from collections import defaultdict
from typing import DefaultDict

from _pytest.nodes import Node


def pytest_addoption(parser):
    group = parser.getgroup("test_this")
    group.addoption(
        "--test-this",
        action="store",
        dest="test_this",
        help='Name of thing to find tests for',
    )


def pytest_collection_modifyitems(config, items):
    symbol = config.getoption('test_this', default=None)
    if symbol is None:
        return False

    files = {x.fspath for x in items}

    results = defaultdict(set)
    for path in files:
        f = LazyFileContents(path)
        find_for_file(
            f=f,
            full_path=path,
            results=results,
            symbol=symbol,
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

    symbol = config.getoption('test_this', default=None)
    if symbol is None:
        return False

    f = LazyFileContents(path)

    # let's just do the quick check here
    if symbol not in f.contents:
        return True


def check_line(*, i, line, symbol, full_path, f, results: DefaultDict[str, set]):
    if re.search(rf'\b{symbol}\b', line):
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


def find_for_file(*, f, full_path, results: DefaultDict[str, set], symbol):
    if symbol in f.contents:
        for i, line in enumerate(f.lines):
            check_line(
                i=i,
                line=line,
                symbol=symbol,
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
