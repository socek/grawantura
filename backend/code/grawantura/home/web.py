from datetime import datetime

from grawantura.main.web import WebEndpoint


@WebEndpoint
async def home(request):
    return {
        "status": "running",
        "time": datetime.now().isoformat(),
    }
