import asyncio
from quart import render_template
from typing import Any


class MWebTemplate:

    async def render(self, template_name_or_list: str | list[str], **context: Any):
        return await render_template(template_name_or_list, **context)

    def sync_render(self, template_name_or_list: str | list[str], **context: Any):
        return asyncio.run(render_template(template_name_or_list=template_name_or_list, **context))


template = MWebTemplate()
