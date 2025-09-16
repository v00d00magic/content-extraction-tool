from app.App import app
from app.AppConsole import call

app.loop.run_until_complete(call())
