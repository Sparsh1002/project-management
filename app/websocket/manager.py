from fastapi import (
    APIRouter,
    WebSocket
)

import json

websocket_router = APIRouter()

active_connections = []


async def broadcast_event(
    event_type: str,
    data: dict
):

    message = json.dumps({
        "event": event_type,
        "data": data
    })

    for connection in active_connections:

        await connection.send_text(message)


@websocket_router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket
):

    await websocket.accept()

    active_connections.append(websocket)

    try:

        while True:

            await websocket.receive_text()

    except:

        active_connections.remove(websocket)