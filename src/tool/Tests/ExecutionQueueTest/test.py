from Plugins.App.Views.CLI.CLI import CLI
import json

cli = CLI(name="cli")

# Single mode
'''
cli.app.app.argv = {
    "i": "Data.Text",
    "text": "^_^",
}
'''
# Getting random number
'''
cli.app.app.argv = {
    "i": "Data.Random",
    "min": 0,
    "max": 100000
}
'''
# Random URL
cli.app.app.argv = {
    "i": json.dumps(
    {
        "return_from": 'join',
        "repeat": 1,
        "pre": [
            {
                "name": "App.Arguments.Types.IntArgument.IntArgument",
                "arguments": {
                    "name": "random",
                    "current": 0
                }
            }
        ],
        "items": [
            {
                "type": "executable",
                "name": "Data.Random.Random",
                "arguments": {
                    "min": 0,
                    "max": 10000
                }
            },
            {
                "type": "executable",
                "name": "Web.URL.URL",
                "arguments": {
                    "url": {
                        "value": "https://example.com/.jpeg",
                        "replacements": [{
                            "position": (33, 33),
                            "value": "#0"
                        }]
                    }
                }
            }
        ]
    })
}
cli.app.loop_with_argv()
