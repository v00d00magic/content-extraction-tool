from declarable.Arguments import StringArgument
from .. import Implementation as RSS
from executables.list.RSS.Item import Implementation as RSSItem
from app.App import logger

class Implementation(RSS.AbstractReceivation):
    @classmethod
    def declare(cls):
        params = {}
        params["url"] = StringArgument({
            "assertion": {
                "not_null": True,
            },
        })

        return params

    async def execute(self, i = {}):
        import aiohttp, xmltodict
        from utils.MediaUtils import rss_date_parse

        url = i.get("url")
        response_xml = None

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response_xml = await response.text()

        logger.log(f"Called passed URL", section="RSS")

        xmltojson = xmltodict.parse(response_xml)
        rss = xmltojson.get('rss')
        channel = rss.get('channel')

        items = channel.get('item')
        if channel != None:
            try:
                del channel['item']
            except:
                pass

        if i.get("do_collections") == True:
            collection = self.ContentUnit()
            collection.display_name = channel.get('title', 'Untitled')
            collection.description = channel.get('description')
            collection.content = channel
            collection.declared_created_at = rss_date_parse(channel.get("pubDate"))
            collection.source = {
                'type': 'url',
                'content': channel.get('link')
            }
            collection.is_collection = True
            self.addLink(collection)

        total = len(items)
        got = 0
        out_items = await RSSItem().execute({
            "object": items
        })

        for out in out_items:
            out.display_name = out.content_json.get("title", "Untitled")
            out.declared_created_at = rss_date_parse(out.content_json.get("pubDate")).timestamp()

            self.notifyAboutProgress(logger.log(f'Got item with name "{out.display_name}"', section=self.outer.section), got / total)

            got += 1

        return out_items
