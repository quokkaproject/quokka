import pytest
from quokka import create_app


# def pytest_runtest_setup(item):
#     # called for running each test in 'a' directory
#     print ("setting up", item)


@pytest.fixture
def app():
    app = create_app(config='quokka.test_settings',
                     DEBUG=False,
                     test=True,
                     mode='test')
    return app
