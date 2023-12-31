import requests


class StocksClient:
    def __init__(self):
        self.base_url = "http://127.0.0.1:8000"

    def post_order(self, data, long_pending=False):
        headers = {} if not long_pending \
            else {'long_pending': 'True'}
        response = requests.post(f"{self.base_url}/orders/", json=data,
                                 headers=headers)
        return response

    def delete_order(self, order_id):
        response = requests.delete(f"{self.base_url}/orders/{order_id}")
        return response

    def get_orders(self):
        response = requests.get(f"{self.base_url}/orders")
        return response

    def get_order(self, order_id):
        response = requests.get(f"{self.base_url}/orders/{order_id}")
        return response
