from starlette.applications import Starlette

from grawantura.auth.web import get_routes as auth_routes
from grawantura.events.web import get_routes as events_routes
from grawantura.events.ws import get_routes as events_ws_routes
from grawantura.games.web import get_routes as games_routes
from grawantura.home.web import get_routes as home_routes
from grawantura.main.globals import app


def get_routes():
    return (
        list(home_routes("/"))
        + list(events_routes("/events"))
        + list(games_routes("/games"))
        + list(auth_routes("/auth"))
        + list(events_ws_routes("/ws"))
    )


app.start()
webapp = Starlette(
    debug=True,
    routes=get_routes(),
)
