from App import app, logger
from aiohttp import web
import os
import asyncio
import threading

from Utils.Configurable import Configurable
from Executables.list.Executables.Execute.Execute import Implementation as Execute
from DB.Models.Content.StorageUnit import StorageUnit
from Utils.Data.JSON import JSON
from pathlib import Path
from Declarable.Documentation import global_documentation
from App import app as mainApp

mainApp.setup()

mainApp.context = "web"

class WebApp(Configurable):
    @classmethod
    def declareSettings(cls):
        from Declarable.Arguments import StringArgument, IntArgument, BooleanArgument

        locale_keys = {
            "ui.lang.name": {
                "en_US": "Language",
            },
            "ui.name.name": {
                "en_US": "Server name",
            },
            "web.host.name": {
                "en_US": "Host name",
            },
            "web.port.name": {
                "en_US": "Port",
            },
        }
        global_documentation.loadKeys(locale_keys)

        items = {}
        items["ui.lang"] = StringArgument({
            "default": 'en_US',
            "docs": {
                "name": global_documentation.get("ui.lang.name"),
            },
        })
        items["ui.name"] = StringArgument({
            "default": "Content extraction tool",
            "docs": {
                "name": global_documentation.get("ui.name.name"),
            },
        })
        items["web.host"] = StringArgument({
            "default": "127.0.0.1",
            "docs": {
                "name": global_documentation.get("web.host.name"),
            },
        })
        items["web.port"] = IntArgument({
            "default": 12345,
            "docs": {
                "name": global_documentation.get("web.port.name"),
            },
        })
        items["web.debug"] = BooleanArgument({
            "default": True,
        })

        return items
    
    def __init__(self):
        self.updateConfig()

def check_node_modules():
    cwd = Path.cwd()
    cwd_web = Path.joinpath(cwd, "app").joinpath("Views").joinpath("Web")
    dir_js_modules = cwd_web.joinpath("assets").joinpath("js")
    dir_node_modules = dir_js_modules.joinpath("node_modules")

    if dir_node_modules.is_dir() == False:
        os.chdir(str(dir_js_modules))
        os.system("npm install")
        os.chdir(str(cwd))

check_node_modules()

app = web.Application()

async def index(request):
    template = """
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">

            <script src="/static/js/node_modules/umbrellajs/umbrella.js"></script>
            <script src="/static/js/node_modules/@andypf/json-viewer/dist/iife/index.js"></script>
            <script type="text/javascript" src="/static/js/node_modules/dompurify/dist/purify.min.js"></script>
            <script src="/static/js/node_modules/interactjs/dist/interact.js"></script>

        </head>
        <body>
            <div id="app"></div>

            <script type="module" src="/static/js/app.js"></script>
        </body>
    </html>
    """

    return web.Response(
        text=template,
        content_type='text/html')

async def act(request):
    act = Execute()

    return web.json_response(text=JSON.dump({
        "payload": await act.execute_with_validation(await request.post())
    }))

async def static(request):
    path = request.match_info.get('path', '')
    static_dir = os.path.join(os.path.dirname(__file__), "assets")
    static_file = os.path.join(static_dir, path)

    if os.path.exists(static_file) and os.path.isfile(static_file):
        return web.FileResponse(static_file)

    return web.HTTPNotFound(text="not found")

async def storage_unit_file(request):
    su_id = int(request.match_info.get('id', ''))
    path = request.match_info.get('path', '')

    storage_unit = StorageUnit.ids(su_id)
    if storage_unit == None:
        return web.HTTPNotFound(text="not found")

    storage_path = storage_unit.getStoragePath()
    path_to_file = storage_path / path

    try:
        path_to_file.resolve().relative_to(storage_path.resolve())
    except (ValueError, RuntimeError):
        raise web.HTTPForbidden(reason="access denied")

    if not path_to_file.is_file():
        raise web.HTTPNotFound()

    return web.FileResponse(str(path_to_file))

async def upload(request):
    reader = await request.multipart()

    field = await reader.next()

    name = await field.read(decode=True)
    field = await reader.next()
    filename = field.filename
    size = 0

    su = StorageUnit()
    su.generateHash()
    su.upload_name = filename

    with open(os.path.join(su.path(), filename), 'wb') as f:
        while True:
            chunk = await field.read_chunk()
            if not chunk:
                break
            size += len(chunk)
            f.write(chunk)

async def websocket_connection(request):
    ws = web.WebSocketResponse()

    await ws.prepare(request)

    async def __logger_hook(**kwargs):
        try:
            await ws.send_str(JSON.dump({
                "type": "log",
                "event_index": 0,
                "payload": {"result": kwargs.get("message").data}
            }))
        except Exception as e:
            app.logger.log(e)

    async def __progress_hook_outer(message):
        try:
            await ws.send_str(JSON.dump({
                "type": "progress",
                "event_index": message.index,
                "payload": {"message": message.message.out(), "percentage": message.percentage}
            }))
        except Exception as e:
            print(e)
            pass

    mainApp.add_hook("progress", __progress_hook_outer)
    logger.add_hook("log", __logger_hook)

    async def send_act(data):
        results = None
        payload = {}

        try:
            results = await Execute(data.get("event_index")).execute_with_validation(data.get("payload"))
            payload["result"] = results.display()
        except Exception as e:
            app.logger.log(e)
            payload["error"] = {
                "status_code": 500,
                "exception_name": e.__class__.__name__,
                "message": str(e),
            }

        await ws.send_str(JSON.dump({
            "type": data.get("type"),
            "event_index": data.get("event_index"),
            "payload": payload
        }))

    try:
        async for msg in ws:
            if msg.type != web.WSMsgType.TEXT:
                continue

            data = JSON.parse(msg.data)
            match (data.get("type")):
                case "act":
                    asyncio.get_event_loop().run_in_executor(
                        None, 
                        lambda: asyncio.run(send_act(data)) 
                    )
    finally:
        mainApp.remove_hook("progress", __progress_hook_outer)
        logger.remove_hook("log", __logger_hook)

    return ws

app.router.add_get('/', index)
app.router.add_post('/api/act', act)
app.router.add_post('/upload', upload)
app.router.add_get('/su{id:.*}/{path:.*}', storage_unit_file)
app.router.add_get('/static/{path:.*}', static)
app.router.add_get('/ws', websocket_connection)
