import time
import locust_patch  # noqa: F401, it's locust patch
from locust import task

from locust_plugins.users.socketio import SocketIOUser
from pydantic import ValidationError

from app.models import Order
from tests.api_client import StocksClient

data = {
    "stoks": "EURUSD",
    "quantity": 123,
}


class MyUser(SocketIOUser):
    order_id = ''
    client = StocksClient()
    validation_error = False

    @task
    def my_task(self):
        self.connect('ws://localhost:8000/ws')
        self.start_perf_counter = time.perf_counter()
        response = self.client.post_order(data)
        try:
            Order.model_validate(response.json())
            self.order_id = response.json()['id']
        except ValidationError as e:
            # fail task if validation is failed
            print(e)
            self.environment.events.request.fire(
                request_type="POST",
                name='Validation error on /orders/',
                response_time=0,
                response_length=0,
                exception=e,
                context=self.context(),
            )
            self.validation_error = True

        self.receive_loop()
        self.sleep_with_heartbeat(10)

    def on_message(self, message):
        """
        Wait for message with order_id
        """
        if f'{self.order_id} is EXECUTED' == message \
                and not self.validation_error:
            response_time = (time.perf_counter()-self.start_perf_counter)*1000

            self.environment.events.request.fire(
                request_type="WSR",
                name='EXECUTED msg received',
                response_time=response_time,
                response_length=len(message),
                exception=None,
                context=self.context(),
            )
