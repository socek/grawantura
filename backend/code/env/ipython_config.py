from grawantura.main.globals import app

config = get_config()  # noqa

print("")
print("Starting Grawantura env...")
print("")
app.start()

print("Adding default imports:")

config.InteractiveShellApp.exec_lines = [
    "from uuid import UUID, uuid4",
    "from datetime import datetime, date",
    "from decimal import Decimal",
    "from datetime import date, datetime",
    "from importlib import reload",
    "from grawantura.main.globals import app",
]

print("\t" + "\n\t".join(config.InteractiveShellApp.exec_lines))
print("")
