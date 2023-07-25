from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request
from fastapi.responses import HTMLResponse
import asyncio
import uuid
from pydantic import BaseModel, UUID4
import random


class Order(BaseModel):
    id: UUID4 | None = None
    stoks: str
    quantity: int
    status: str | None = None


class Status:
    pending = 'PENDING'
    cancelled = 'CANCELLED'
    executed = 'EXECUTED'


app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()
orders = {}


@app.get("/")
async def get():
    return HTMLResponse(html)


@app.get("/orders")
async def get():
    return orders


@app.get("/orders/{order_id}")
async def read_order(order_id: str):
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")
    return orders[order_id]


@app.post("/orders/")
async def create_order(order_input: Order, request: Request):
    print(request.headers)
    long_pending = True if request.headers.get('long_ending') else False
    order_input.id = uuid.uuid4()
    order_input.status = Status.pending
    orders[str(order_input.id)] = order_input
    task = asyncio.create_task(
        start_pending_order(
            str(order_input.id),
            long_pending=long_pending
        )
    )
    return order_input


async def start_pending_order(order_id: str, long_pending=False):
    await manager.broadcast(f'{order_id} is {Status.pending}')
    sleep_time = random.uniform(0.1, 1) if not long_pending else 5
    await asyncio.sleep(sleep_time)
    if orders[order_id].status != Status.cancelled:
        orders[order_id].status = Status.executed
        await manager.broadcast(f'{order_id} is {Status.executed}')


@app.delete("/orders/{order_id}", status_code=204)
async def delete_order(order_id: str):
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")
    if orders[order_id].status != Status.executed:
        orders[order_id].status = Status.cancelled
        await manager.broadcast(f'{order_id} is {Status.cancelled}')


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
