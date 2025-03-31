from asyncio import get_running_loop
from asyncio import sleep
from datetime import datetime
from enum import Enum
from enum import auto

from starlette.endpoints import WebSocketEndpoint
from starlette.exceptions import HTTPException
from starlette.routing import WebSocketRoute
from starlette.websockets import WebSocket

from grawantura.auth.jwtsupport import validate_user_id_from_token
from grawantura.events.drivers.queries import get_events
from grawantura.main.web import sanitize


class Status(Enum):
    not_running = auto()
    running = auto()
    stopping = auto()


class WebSockeSession:
    def __init__(self, websocket):
        self.is_validated = False
        self.user_id = None
        self.websocket = websocket
        self.last_time = datetime.now()
        self.running = Status.not_running

    async def send_handshake(self):
        await self.send({"time": self.last_time, "payload": {"type": "handshake"}})

    async def handle(self, websocket, payload):
        match payload["type"]:
            case "handshake":
                await self.handle_handshake(payload)
            case default:
                ic(payload)

    async def handle_handshake(self, payload):
        self.user_id = validate_user_id_from_token(payload["token"])
        self.is_validated = True
        loop = get_running_loop()
        loop.create_task(self.send_events())

    async def send(self, payload: dict):
        await self.websocket.send_json(sanitize(payload))

    async def send_events(self):
        self.running = Status.running
        try:
            while self.running == Status.running:
                events = get_events(self.last_time)
                self.last_time = datetime.now()
                if events:
                    for event in events:
                        await  self.send(event)
                await sleep(0.1)
        finally:
            self.running = Status.not_running

    async def stop(self):
        if self.running != Status.running:
            return
        self.running = Status.stopping
        while self.running != Status.not_running:
            await sleep(0.1)



_sessions = {}


class WSEndpoint(WebSocketEndpoint):
    encoding = "json"

    async def on_connect(self, websocket: WebSocket):
        await websocket.accept()
        _sessions[websocket.client.port] = WebSockeSession(websocket)
        await _sessions[websocket.client.port].send_handshake()

    async def on_receive(self, websocket: WebSocket, payload: dict):
        await _sessions[websocket.client.port].handle(websocket, payload)

    async def on_disconnect(self, websocket: WebSocket, close_code: int):
        await _sessions[websocket.client.port].stop()
        del _sessions[websocket.client.port]


def get_routes(prefix: str):
    yield WebSocketRoute(prefix, WSEndpoint)
