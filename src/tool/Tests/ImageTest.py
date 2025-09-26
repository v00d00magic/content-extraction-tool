from App.AppConsole import call
from App import app

app.argv = {
    'i': 'Files.Image',
    'url': 'https://www.booksite.ru/fulltext/1/001/010/001/280082551.jpg',
}

app.loop.run_until_complete(call())
