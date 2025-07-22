import asyncio
from datetime import datetime
from quart import render_template, make_response, send_from_directory, Response
from typing import Any
from quart.typing import FilePath
from mw_common import HTTPContentType


class MWebResponse:

    @classmethod
    async def render_template(cls, template_name_or_list: str | list[str], **context: Any):
        return await render_template(template_name_or_list, **context)

    @classmethod
    def sync_render_template(cls, template_name_or_list: str | list[str], **context: Any):
        return asyncio.run(render_template(template_name_or_list=template_name_or_list, **context))

    @classmethod
    async def make_response(cls, content: str | dict | list, headers: dict = None, http_code: int = None):
        if http_code is None:
            http_code = 200
        response = await make_response(content, http_code)
        if headers:
            response.headers.update(headers)
        return response

    @classmethod
    async def json_response(cls, content: dict | list, headers: dict = None, http_code: int = None):
        if not http_code:
            http_code = 200

        if not headers:
            headers = {}

        headers["Content-Type"] = HTTPContentType.APPLICATION_UNICODE_JSON
        return await MWebResponse.make_response(content=content, headers=headers, http_code=http_code)

    @classmethod
    async def send_from_directory(cls, directory: FilePath, file_name: str, mimetype: str | None = None, as_attachment: bool = False, attachment_filename: str | None = None, add_etags: bool = True, cache_timeout: int | None = None, conditional: bool = True, last_modified: datetime | None = None) -> Response:
        return await send_from_directory(
            directory=directory,
            file_name=file_name,
            mimetype=mimetype,
            as_attachment=as_attachment,
            attachment_filename=attachment_filename,
            add_etags=add_etags,
            cache_timeout=cache_timeout,
            conditional=conditional,
            last_modified=last_modified
        )
