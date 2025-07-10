from quart import Quart
from typing import Any
import asyncio
import warnings
import os
import signal
from quart.utils import observe_changes, MustReloadError, restart
from quart.app import _cancel_all_tasks
from quart.helpers import get_debug_flag
from mw_common.mw_console_log import Console
from mw_common.mw_exception import MwException
from mweb import BaseController


class MWebBase(Quart):

    def register_controller(self, controller: BaseController):
        self.register_blueprint(controller)

    def register_exception_handler(self, exception_class: type[MwException], handler):
        self.register_error_handler(exception_class, handler)

    def run(
            self,
            host: str | None = None,
            port: int | None = None,
            debug: bool | None = None,
            use_reloader: bool = True,
            loop: asyncio.AbstractEventLoop | None = None,
            ca_certs: str | None = None,
            certfile: str | None = None,
            keyfile: str | None = None,
            **kwargs: Any,
    ) -> None:
        """Run this application.

        This is best used for development only, see Hypercorn for
        production servers.

        Arguments:
            host: Hostname to listen on. By default this is loopback
                only, use 0.0.0.0 to have the server listen externally.
            port: Port number to listen on.
            debug: If set enable (or disable) debug mode and debug output.
            use_reloader: Automatically reload on code changes.
            loop: Asyncio loop to create the server in, if None, take default one.
                If specified it is the caller's responsibility to close and cleanup the
                loop.
            ca_certs: Path to the SSL CA certificate file.
            certfile: Path to the SSL certificate file.
            keyfile: Path to the SSL key file.
        """
        if kwargs:
            warnings.warn(
                f"Additional arguments, {','.join(kwargs.keys())}, are not supported.\n"
                "They may be supported by Hypercorn, which is the ASGI server Quart "
                "uses by default. This method is meant for development and debugging.",
                stacklevel=2,
            )

        if loop is None:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        if "QUART_DEBUG" in os.environ:
            self.debug = get_debug_flag()

        if debug is not None:
            self.debug = debug

        loop.set_debug(self.debug)

        shutdown_event = asyncio.Event()

        def _signal_handler(*_: Any) -> None:
            shutdown_event.set()

        for signal_name in {"SIGINT", "SIGTERM", "SIGBREAK"}:
            if hasattr(signal, signal_name):
                try:
                    loop.add_signal_handler(
                        getattr(signal, signal_name), _signal_handler
                    )
                except NotImplementedError:
                    # Add signal handler may not be implemented on Windows
                    signal.signal(getattr(signal, signal_name), _signal_handler)

        server_name = self.config.get("SERVER_NAME")
        sn_host = None
        sn_port = None
        if server_name is not None:
            sn_host, _, sn_port = server_name.partition(":")

        if host is None:
            host = sn_host or "127.0.0.1"

        if port is None:
            port = int(sn_port or "5000")

        task = self.run_task(
            host,
            port,
            debug,
            ca_certs,
            certfile,
            keyfile,
            shutdown_trigger=shutdown_event.wait,  # type: ignore
        )

        Console.info(f"Serving MWeb App '{self.name}'", system_log=True) # noqa: T201
        Console.info(f"Debug mode: {self.debug or False}", system_log=True)  # noqa: T201
        Console.info("Please use an ASGI server (e.g. Hypercorn) directly in production", system_log=True)  # noqa: T201
        scheme = "https" if certfile is not None and keyfile is not None else "http"
        Console.info(f"Running on {scheme}://{host}:{port} (CTRL + C to quit)", system_log=True)  # noqa: T201

        tasks = [loop.create_task(task)]

        if use_reloader:
            tasks.append(
                loop.create_task(observe_changes(asyncio.sleep, shutdown_event))
            )

        reload_ = False
        try:
            loop.run_until_complete(asyncio.gather(*tasks))
        except MustReloadError:
            reload_ = True
        finally:
            try:
                _cancel_all_tasks(loop)
                loop.run_until_complete(loop.shutdown_asyncgens())
            finally:
                asyncio.set_event_loop(None)
                loop.close()

        if reload_:
            restart()
