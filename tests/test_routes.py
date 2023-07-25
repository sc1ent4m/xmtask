import pytest
from time import sleep

from server import Status


data = {
    "stoks": "EURUSD",
    "quantity": 123,
}
uniq_data = {
    "stoks": "USDEUR",
    "quantity": 234,
}
wrong_data = {
    "foo": "12",
    "bar": "13"
}


@pytest.fixture()
def send_orders(stocks_client):
    stocks_client.post_order(data)
    stocks_client.post_order(data)


def test_get_orders(stocks_client, send_orders):
    responce = stocks_client.get_orders()
    orders = responce.json()
    assert len(orders) == 2
    for order, value in orders.items():
        assert value['id']
        assert value['status'] == Status.pending


def test_get_order(stocks_client):
    id = stocks_client.post_order(uniq_data).json()['id']
    responce = stocks_client.get_order(id).json()
    assert responce['id'] == id
    assert responce['stoks'] == 'USDEUR'
    assert responce['quantity'] == 234
    assert responce['status'] == Status.pending


def test_post_wrong_order(stocks_client):
    response = stocks_client.post_order(wrong_data)
    assert response.status_code == 422


def test_get_unexisted_order(stocks_client):
    response = stocks_client.get_order('123123')
    assert response.status_code == 404


def test_delete_order(stocks_client):
    order = stocks_client.post_order(data, long_pending=True).json()
    delete_response = stocks_client.delete_order(order['id'])
    assert delete_response.status_code == 204
    response = stocks_client.get_order(order['id']).json()
    assert response['status'] == Status.cancelled


def test_delete_unknown_order(stocks_client):
    response = stocks_client.delete_order('123123')
    assert response.status_code == 404


def test_delete_executed_order(stocks_client):
    order_id = stocks_client.post_order(data).json()['id']
    sleep(1)
    assert stocks_client.get_order(order_id).json()['status'] == 'EXECUTED'
    stocks_client.delete_order(order_id)
    assert stocks_client.get_order(order_id).json()['status'] == 'EXECUTED'
