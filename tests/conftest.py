import pytest
from tests.api_client import StocksClient
from websockets.sync.client import connect


@pytest.fixture(scope='session')
def stocks_client():
    yield StocksClient()


@pytest.fixture()
def websocket_client():
    client = connect('ws://localhost:8000/ws')
    yield client
    client.close()
