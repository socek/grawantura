from starlette.applications import Starlette
from starlette.routing import Route

from grawantura.events.web import events
from grawantura.games.web import create_game
from grawantura.games.web import games
from grawantura.games.web import update_game
from grawantura.home.web import home
from grawantura.main.globals import app

routes = [
    Route("/", home),
    Route("/games", games, methods=['GET']),
    Route("/games", create_game, methods=['POST']),
    Route("/games", update_game, methods=['PATCH']),
    Route("/events", events),
]
app.start()


webapp = Starlette(
    debug=True,
    routes=routes,
)
