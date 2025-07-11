import asyncio
from quart import render_template, make_response
from typing import Any
from mw_common import HTTPContentType


class MWebResponse:

    @staticmethod
    async def render_template(template_name_or_list: str | list[str], **context: Any):
        return await render_template(template_name_or_list, **context)

    @staticmethod
    def sync_render_template(template_name_or_list: str | list[str], **context: Any):
        return asyncio.run(render_template(template_name_or_list=template_name_or_list, **context))

    @staticmethod
    async def make_response(content: str | dict | list, headers: dict = None, http_code: int = None):
        if http_code is None:
            http_code = 200
        response = await make_response(content, http_code)
        if headers:
            response.headers.update(headers)
        return response

    @staticmethod
    async def json_response(content: dict | list, headers: dict = None, http_code: int = None):
        if not http_code:
            http_code = 200

        if not headers:
            headers = {}

        headers["Content-Type"] = HTTPContentType.APPLICATION_UNICODE_JSON
        return await MWebResponse.make_response(content=content, headers=headers, http_code=http_code)
