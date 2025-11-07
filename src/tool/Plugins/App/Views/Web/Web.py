from ..View import View
from Plugins.Data.NameDictList import NameDictList
from Plugins.App.Arguments.Types.StringArgument import StringArgument
from Plugins.App.Arguments.Types.IntArgument import IntArgument
from Plugins.App.Arguments.Types.BooleanArgument import BooleanArgument

from Objects.Configurable import Configurable

from Objects.ClassProperty import classproperty
from pathlib import Path
from aiohttp import web as aiohttp_web
import os

class Web(View):
    class Wrapper(View.Wrapper, Configurable):
        def constructor(self):
            self.ws = []
            self.app = aiohttp_web.Application()
            self.addRoutes(self.routes)

        def addRoutes(self, routes: list):
            for route in routes:
                getattr(self.app.router, f"add_{route[2]}")(route[0], route[1])

        @property
        def routes(self):
            return [
                ('/', self.SPA, 'get'),
                ('/static/{path:.*}', self.getAsset, 'get'),
                ('/storage/{id:.*}/{path:.*}', self.getStorageUnit, 'get'),
                ('/api/execute', self.getExecuteResults, 'post'),
                ('/rpc', self.getWSConnection, 'get'),
                ('/api/upload', self.uploadAsStorageUnit, 'post')
            ]

        def SPA(self, request):
            cdn_libs = [
                "https://cdn.jsdelivr.net/npm/umbrellajs"
            ]
            html = """
            <!DOCTYPE html><html>
                <head>
                    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
            """

            for lib in cdn_libs:
                html += f"<script src=\"{lib}\" type=\"text/javascript\"></script>"

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

        async def getExecuteResults(self, request):
            pass

        async def getWSConnection(self, request):
            response = aiohttp_web.WebSocketResponse()
            await response.prepare(request)

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
                pass

            return ws

        async def getAsset(self, request):
            asset_path  = request.match_info.get('path', '')
            static_dir  = Path(os.path.dirname(__file__)).joinpath("assets")
            static_file = static_dir.joinpath(asset_path)
            if static_file.exists() == True and static_file.is_file() == True:
                return aiohttp_web.FileResponse(static_file)

            return aiohttp_web.HTTPNotFound(text="Asset not found")

        async def uploadAsStorageUnit(self, request):
            # TODO
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

        async def getStorageUnit(self, request):
            # TODO
            unit_id = int(request.match_info.get('id', ''))
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

        @classproperty
        def options(cls) -> NameDictList:
            print("get")
            return NameDictList([
                StringArgument(
                    name = 'ui.lang',
                    default = 'en_US'
                ),
                StringArgument(
                    name = 'ui.name',
                    default = 'CET'
                ),
                StringArgument(
                    name = 'aiohttp.host',
                    default = '127.0.0.1'
                ),
                IntArgument(
                    name = 'aiohttp.port',
                    default = 35208
                ),
                BooleanArgument(
                    name = 'web.debug',
                    default = True
                )
            ])

    def run(self):
        # workaround
        self.subclass.applyToGlobalSettings()
        aiohttp_web.run_app(self.subclass.app,
            host=self.app.app.Config.get("aiohttp.host"),
            port=self.app.app.Config.get("aiohttp.port"),
        )
