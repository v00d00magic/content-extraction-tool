from Views.CLI import CLI
from Executables.list.Content.Search.ContentUnits import Implementation as Search

cli = CLI()

# Export first 10 found items

async def _call():
    search = Search.makeSelfCall()
    search.passArgs({
        "count": 10
    })

    output = await search.run_asyncely()
    items = output.data.get("items")
    items_outputs = []

    for item in items:
        items_outputs.append({
            "class_name": item.short_name,
            "id": item.uuid
        })

    cli.app.argv = {
        "i": "Content.Movement.Export",
        "items": items_outputs
    }

    await cli.call()

cli.app.loop.run_until_complete(_call())
