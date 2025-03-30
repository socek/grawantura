from grawantura.games.drivers import commands
from grawantura.games.drivers.queries import get_games
from grawantura.main.web import WebEndpoint


@WebEndpoint
async def games(request):
    return {
        "items": get_games(),
    }


@WebEndpoint
async def create_game(request):
    payload = await request.json()
    commands.create_game(name=payload["name"])
    return {
        "status": "success",
    }


@WebEndpoint
async def update_game(request):
    payload = await request.json()
    commands.update_game(
        game_id=payload["game_id"],
        name=payload["name"],
    )
    return {
        "status": "success",
    }
