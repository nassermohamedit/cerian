import pytest


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "nonrepeatable: Test might fail unexpectedly"
    )
    config.addinivalue_line(
        "markers", "slow: Slow test"
    )
