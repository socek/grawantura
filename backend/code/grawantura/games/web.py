from grawantura.games.drivers.queries import get_games
from grawantura.main.web import WebEndoint


@WebEndoint
async def games(request):
    return {
        "items": get_games(),
    }
