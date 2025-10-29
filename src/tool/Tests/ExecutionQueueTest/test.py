from Plugins.App.Views.CLI.CLI import CLI
import json

cli = CLI(name="cli")

# Single mode
'''cli.app_wrapper.app.argv = {
    "i": "Data.Text",
    "text": "^_^",
}'''
# Getting random number
cli.app_wrapper.app.argv = {
    "i": "Data.Random",
    "min": 0,
    "max": 100000
}
# Creating text from random numbers
'''cli.app_wrapper.app.argv = {
    "i": json.dumps(
    [
        {
            "name": "Data.Random",

        }
    ])
}'''
cli.loopSelfAndRunExecute()
