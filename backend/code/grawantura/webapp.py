from datetime import datetime

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

from grawantura.main.globals import app


async def home(request):
    return JSONResponse(
        {
            "status": "running",
            "time": datetime.now().isoformat(),
        }
    )


app.start()
webapp = Starlette(
    debug=True,
    routes=[
        Route("/", home),
    ],
)
