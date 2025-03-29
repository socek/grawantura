from starlette.applications import Starlette
from starlette.routing import Route

from grawantura.games.web import games
from grawantura.home.web import home
from grawantura.main.globals import app

routes = [
    Route("/", home),
    Route("/games", games)
]

app.start()
webapp = Starlette(
    debug=True,
    routes=routes,
)
