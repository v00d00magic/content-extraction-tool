from aiohttp import web as aiohttp_web
import os
import asyncio
from DB.Models.Content.StorageUnit import StorageUnit

from Utils.Configurable import Configurable
from Executables.list.Executables.Execute.Execute import Implementation as Execute
from Executables.ExecutableCall import ExecutableCall
from Utils.Data.JSON import JSON
from pathlib import Path
from Declarable.Documentation import global_documentation
from App.App import App

class WebApp(Configurable):
    def __init__(self):
        self.ws = []
        self.app = App("web")
        self.app.setup()
        self.web_app = aiohttp_web.Application()
        self.updateConfig()
        # self._checkNodeModules()
        self._registerRoutes()    
        # self._registerHooks()

    def _checkNodeModules(self):
        cwd = Path.cwd()
        cwd_web = cwd.joinpath("Views").joinpath("Web")
        js_modules = cwd_web.joinpath("assets").joinpath("js")
        node_modules = js_modules.joinpath("node_modules")

        if node_modules.is_dir() == False:
            os.chdir(str(js_modules))
            os.system("npm install")
            os.chdir(str(cwd))

    def _registerRoutes(self):
        self.web_app.router.add_get('/', self.showSPAIndex)
        self.web_app.router.add_post('/api/act', self.runExecute)
        self.web_app.router.add_post('/api/upload', self.uploadStorageUnit)
        self.web_app.router.add_get('/api/ws', self.wsConnection)
        self.web_app.router.add_get('/storage/su{id:.*}/{path:.*}', self.returnStorageUnitPath)
        self.web_app.router.add_get('/storage/static/{path:.*}', self.returnStaticWebAsset)

    def _registerHooks(self):
        async def loggerHook(**kwargs):
            try:
                '''await ws.send_str(JSON.dump({
                    "type": "log",
                    "event_index": 0,
                    "payload": {"result": kwargs.get("message").data}
                }))'''
                pass
            except Exception as e:
                self.app.logger.log(e)

        self.app.logger.add_hook("log", loggerHook)

    def run(self):
        aiohttp_web.run_app(self.web_app,
            host=self.app.config.get("web.host"),
            port=self.app.config.get("web.port"),
        )

    async def showSPAIndex(self, request):
        libs = [
            "umbrellajs/umbrella.js",
            "@andypf/json-viewer/dist/iife/index.js",
            "dompurify/dist/purify.min.js",
            "interactjs/dist/interact.js"
        ]

        html = """
        <!DOCTYPE html>
        <html>
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
        """

        for lib in libs:
            html += f"<script src=\"/storage/static/js/node_modules/{lib}\" type=\"text/javascript\"></script>"

        html += """
            </head>
            <body>
                <div id="app"></div>

                <script type="module" src="/storage/static/js/app/Init.js"></script>
            </body>
        </html>
        """

        return aiohttp_web.Response(
            text = html,
            content_type = 'text/html'
        )

    async def runExecute(self, request):
        act = Execute()

        return aiohttp_web.json_response(text=JSON.dump({
            "payload": await act.execute_with_validation(await request.post())
        }))

    async def returnStaticWebAsset(self, request):
        path = request.match_info.get('path', '')
        static_dir = Path(os.path.dirname(__file__)).joinpath("assets")
        static_file = Path(static_dir).joinpath(path)

        if static_file.exists() == True and static_file.is_file() == True:
            return aiohttp_web.FileResponse(static_file)

        return aiohttp_web.HTTPNotFound(text="Asset did not found :(")

    async def returnStorageUnitPath(self, request):
        sid = int(request.match_info.get('id', ''))
        path = request.match_info.get('path', '')
        storage_unit = StorageUnit.ids(sid)
        if storage_unit == None:
            return aiohttp_web.HTTPNotFound(text="Not found storage unit with this id")

        storage_path = storage_unit.hash_dir.upper()
        file = storage_path / path

        try:
            file.resolve().relative_to(storage_path.resolve())
        except (ValueError, RuntimeError):
            raise aiohttp_web.HTTPForbidden(reason="Access denied")

        if not file.is_file():
            raise aiohttp_web.HTTPNotFound(text="Storage unit found but path is not")

        return aiohttp_web.FileResponse(str(file))

    async def uploadStorageUnit(self, request):
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

    async def wsConnection(self, request):
        ws = aiohttp_web.WebSocketResponse()

        await ws.prepare(request)

        async def progressHook(message):
            try:
                await ws.send_str(JSON.dump({
                    "type": "progress",
                    "event_index": message.index,
                    "payload": {"message": message.message.out(), "percentage": message.percentage}
                }))
            except Exception as e:
                print(e)
                pass

        self.app.add_hook("progress", progressHook)

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
            self.app.remove_hook("progress", __progress_hook_outer)
            logger.remove_hook("log", __logger_hook)

        return ws

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
            "default": 35208,
            "docs": {
                "name": global_documentation.get("web.port.name"),
            },
        })
        items["web.debug"] = BooleanArgument({
            "default": True,
        })

        return items
