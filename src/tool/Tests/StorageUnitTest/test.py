from Plugins.App.Views.CLI.CLI import CLI
import json

cli = CLI(name="cli")
cli.app.app.argv = {
    "i": json.dumps(
        {
            "return_from": 'join',
            "repeat": 10,
            "items": [
                {
                    "name": "Data.Random.Random",
                    "arguments": {
                        "min": 0,
                        "max": 10000
                    }
                }
            ]
        }
    )
}
cli.app.loop_with_argv()
