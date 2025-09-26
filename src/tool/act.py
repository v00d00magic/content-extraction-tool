from Views.CLI import CLI

cli = CLI()

cli.app.loop.run_until_complete(cli.call())
