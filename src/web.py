from app.App import config
from app.Views.Web import app
import aiohttp, asyncio

aiohttp.web.run_app(app,
    host=config.get("web.host"),
    port=config.get("web.port"),
)
