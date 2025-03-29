from contextlib import asynccontextmanager

from starlette.applications import Starlette
from starlette.routing import Route

from grawantura.events.web import events
from grawantura.games.web import games
from grawantura.home.web import home
from grawantura.main.globals import app

routes = [
    Route("/", home),
    Route("/games", games),
    Route("/events", events),
]
app.start()


webapp = Starlette(
    debug=True,
    routes=routes,
)
