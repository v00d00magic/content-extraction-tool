from Plugins.App.Views.CLI.CLI import CLI

cli = CLI(name="cli")

# Single mode
cli.app_wrapper.app.argv = {
    "i": "Data.Text",
    "text": "^_^",
}
cli.loopSelfAndRunExecute()
