from datetime import datetime

from grawantura.main.web import WebEndoint


@WebEndoint
async def home(request):
    return {
        "status": "running",
        "time": datetime.now().isoformat(),
    }
