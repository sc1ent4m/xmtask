from time import sleep


data = {
    "stoks": "EURUSD",
    "quantity": 123,
}


def test_websocket_standart_flow(websocket_client, stocks_client):
    order_id = stocks_client.post_order(data, long_pending=True).json()['id']
    ws_message = websocket_client.recv(timeout=10)
    assert f'{order_id} is PENDING' == ws_message
    sleep(5)
    ws_message = websocket_client.recv(timeout=10)
    assert f'{order_id} is EXECUTED' == ws_message


def test_websocket_delete_flow(websocket_client, stocks_client):
    order_id = stocks_client.post_order(data, long_pending=True).json()['id']
    ws_message = websocket_client.recv(timeout=10)
    assert f'{order_id} is PENDING' == ws_message
    stocks_client.delete_order(order_id)
    ws_message = websocket_client.recv(timeout=10)
    assert f'{order_id} is CANCELLED' == ws_message
