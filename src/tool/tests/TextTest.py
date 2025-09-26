from app.AppConsole import call
from app.App import app

app.argv = {
    'i': 'Abstract.Text',
    'text': '123456',
}

app.loop.run_until_complete(call())
