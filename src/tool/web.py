from App import app
from Views.Web import app
import aiohttp, asyncio

aiohttp.web.run_app(app,
    host=config.get("web.host"),
    port=config.get("web.port"),
)
