from starlette.applications import Starlette
from starlette.routing import Route

from grawantura.events.web import events
from grawantura.games import web
from grawantura.home.web import home
from grawantura.main.globals import app


def get_routes():
    routes = [
        Route("/", home),
        Route("/events", events),
    ]
    return (
        routes
        + list(web.get_routes("/games"))
    )


app.start()
webapp = Starlette(
    debug=True,
    routes=get_routes(),
)
