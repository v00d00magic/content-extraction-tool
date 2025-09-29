from Views.CLI import CLI

cli = CLI()
cli.app.argv = {
    'i': 'Files.Image',
    'url': 'https://www.booksite.ru/fulltext/1/001/010/001/280082551.jpg',
}

cli.app.loop.run_until_complete(cli.call())
