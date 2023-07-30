import asyncio
import uuid
import random

from fastapi import FastAPI, WebSocket, WebSocketDisconnect,\
    HTTPException, Request

from .models import Order


class Status:
    pending = 'PENDING'
    cancelled = 'CANCELLED'
    executed = 'EXECUTED'


app = FastAPI()


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


@app.get("/orders")
async def get_orders():
    await asyncio.sleep(random.uniform(0.1, 1))
    return orders


@app.get("/orders/{order_id}")
async def read_order(order_id: str):
    await asyncio.sleep(random.uniform(0.1, 1))
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
    asyncio.create_task(  # random short delay
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
        await asyncio.sleep(random.uniform(0.1, 1))


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)
