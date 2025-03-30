from grawantura.main.globals import app

print("")
print("Starting Grawantura env...")
print("")
app.start()

print("Adding default imports:")
config = get_config()  # noqa

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
