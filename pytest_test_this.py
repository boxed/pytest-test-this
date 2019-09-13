import pytest


def pytest_addoption(parser):
    group = parser.getgroup("test_this")
    group.addoption(
        "--test-this",
        action="store",
        dest="test_this",
        help='Name of thing to find tests for',
    )
