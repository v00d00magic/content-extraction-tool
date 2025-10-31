from Plugins.App.Views.CLI.CLI import CLI
import json

cli = CLI(name="cli")

# Single mode
'''
cli.app_wrapper.app.argv = {
    "i": "Data.Text",
    "text": "^_^",
}
'''
# Getting random number
'''
cli.app_wrapper.app.argv = {
    "i": "Data.Random",
    "min": 0,
    "max": 100000
}
'''
# Random URL
cli.app_wrapper.app.argv = {
    "i": json.dumps(
    {
        "return_from": -1,
        "variables": [],
        "items": [
            {
                "name": "Data.Random",
                "arguments": {
                    "min": 0,
                    "max": 10000
                }
            },
            {
                "name": "Web.URL",
                "arguments": {
                    "url": {
                        "value": "https://example.com/.jpeg",
                        "replacements": [{
                            "position": (33, 33),
                            "value": "$0.data.$0.content.number"
                        }]
                    }
                }
            }
        ]
    })
}
cli.loopSelfAndRunExecute()
