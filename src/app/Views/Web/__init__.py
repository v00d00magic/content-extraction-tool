from resources.Consts import consts
from app.App import config, logger
from aiohttp import web
import os

from executables.list.Executables.ActsRun import Implementation as RunAct
from db.Models.Content.StorageUnit import StorageUnit
from utils.MainUtils import dump_json, parse_json
from pathlib import Path
from app.App import app as orig_app

orig_app.setup()
consts["context"] = "web"

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

async def _act(args):
    act = RunAct()

    return await act.execute_with_validation(args)

async def act(request):
    return web.json_response(text=dump_json({
        "payload": await _act(await request.post())
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

    storage_path = storage_unit.dir_path()
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
            chunk = await field.read_chunk()  # 8192 bytes by default.
            if not chunk:
                break
            size += len(chunk)
            f.write(chunk)

async def websocket_connection(request):
    ws = web.WebSocketResponse()

    logger.log(message=f"Started WebSocket connection", kind=logger.KIND_MESSAGE, section=logger.SECTION_WEB)

    async def __logger_hook(**kwargs):
        try:
            await ws.send_str(dump_json({
                "type": "log",
                "event_index": 0,
                "payload": {"result": kwargs.get("message").data}
            }))
        except Exception:
            pass

    logger.add_hook("log", __logger_hook)

    await ws.prepare(request)

    async for msg in ws:
        if msg.type != web.WSMsgType.TEXT:
            continue

        data = parse_json(msg.data)
        match (data.get("type")):
            case "act":
                results = None
                payload = {}

                try:
                    results = await _act(data.get("payload"))
                    payload["result"] = results
                except Exception as e:
                    logger.log(e)
                    payload["error"] = {
                        "status_code": 500,
                        "exception_name": e.__class__.__name__,
                        "message": str(e),
                    }

                await ws.send_str(dump_json({
                    "type": data.get("type"),
                    "event_index": data.get("event_index"),
                    "payload": payload
                }))

    return ws

app.router.add_get('/', index)
app.router.add_post('/api/act', act)
app.router.add_post('/upload', upload)
app.router.add_get('/su{id:.*}/{path:.*}', storage_unit_file)
app.router.add_get('/static/{path:.*}', static)
app.router.add_get('/ws', websocket_connection)
