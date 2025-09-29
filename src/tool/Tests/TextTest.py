from Views.CLI import CLI

cli = CLI()
cli.app.argv = {
    'i': 'Abstract.Text',
    'text': '123456',
}

cli.app.loop.run_until_complete(cli.call())
