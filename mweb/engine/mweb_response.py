import asyncio
import csv
import os
from datetime import datetime
from io import BytesIO, StringIO
from pathlib import Path

from quart import render_template, make_response, send_from_directory, Response, send_file, render_template_string
from typing import Any
from quart.typing import FilePath
from mw_common import HTTPContentType, MwException


class MWebResponse:

    @classmethod
    async def render_template(cls, template_name_or_list: str | list[str], **context: Any):
        return await render_template(template_name_or_list, **context)

    @classmethod
    async def render_template_string(cls, source: str, **context: Any):
        return await render_template_string(source, **context)

    @classmethod
    def sync_render_template(cls, template_name_or_list: str | list[str], **context: Any):
        return asyncio.run(render_template(template_name_or_list=template_name_or_list, **context))

    @classmethod
    async def make_response(cls, content: str | dict | list, headers: dict | None = None, http_code: int | None = None):
        if http_code is None:
            http_code = 200
        response = await make_response(content, http_code)
        if headers:
            response.headers.update(headers)
        return response

    @classmethod
    async def make_text_response(cls, content: str, headers: dict | None = None, http_code: int | None = None):
        if not headers:
            headers = {}
        headers["Content-Type"] = "text/plain; charset=utf-8"
        return await cls.make_response(content=content, headers=headers, http_code=http_code)

    @classmethod
    async def send_file(cls, filename_or_io: FilePath | BytesIO, mimetype: str | None = None, as_attachment: bool = False, attachment_filename: str | None = None, headers: dict | None = None, http_code: int | None = None):
        if http_code is None:
            http_code = 200
        response = await send_file(
            filename_or_io=filename_or_io,
            mimetype=mimetype,
            as_attachment=as_attachment,
            attachment_filename=attachment_filename
        )
        response.status_code = http_code
        if headers:
            response.headers.update(headers)
        return response

    @classmethod
    async def json_response(cls, content: str | dict | list, headers: dict | None = None, http_code: int | None = None):
        if not http_code:
            http_code = 200

        if not headers:
            headers = {}

        headers["Content-Type"] = HTTPContentType.APPLICATION_UNICODE_JSON
        return await cls.make_response(content=content, headers=headers, http_code=http_code)

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

    @classmethod
    async def response_pdf(cls, bytes_content: bytes | None = None, file_path: str | None = None, download: bool = True, filename: str | None = None):
        if not bytes_content and not file_path:
            raise MwException("Either bytes_content or file_path must be provided.")

        if not filename:
            if file_path:
                filename = os.path.basename(file_path)
            else:
                filename = "document.pdf"
        elif filename:
            filename = f"{filename}.pdf"

        if file_path:
            if not os.path.exists(file_path):
                raise MwException(f"PDF file not found: {file_path}")
            pdf_source = file_path
        else:
            pdf_source = BytesIO(bytes_content)

        return await cls.send_file(
            filename_or_io=pdf_source,
            mimetype="application/pdf",
            as_attachment=download,
            attachment_filename=filename,
            headers={"Access-Control-Expose-Headers": "Content-Disposition"}
        )

    @classmethod
    async def response(cls, content, status: int | None = None, headers: dict | None = None, mimetype: str | None = None, content_type: str | None = None) -> Response:
        return Response(content, status=status, headers=headers, mimetype=mimetype, content_type=content_type)

    @classmethod
    async def response_csv(cls, rows: list[list], filename: str = "data"):
        output = StringIO()
        writer = csv.writer(output)
        writer.writerows(rows)

        csv_data = f"\ufeff{output.getvalue()}"
        output.close()

        csv_bytes = csv_data.encode("utf-8")
        return await cls.send_file(
            filename_or_io=BytesIO(csv_bytes),
            mimetype="text/csv",
            as_attachment=True,
            attachment_filename=f"{filename}.csv",
            headers={"Access-Control-Expose-Headers": "Content-Disposition"}
        )

    @classmethod
    async def response_zip(cls, bytes_content: bytes, filename: str = "unknown"):
        filename = Path(filename).name.removesuffix(".zip")
        return await cls.send_file(
            filename_or_io=BytesIO(bytes_content),
            mimetype="application/zip",
            as_attachment=True,
            attachment_filename=f"{filename}.zip",
            headers={"Access-Control-Expose-Headers": "Content-Disposition"}
        )
