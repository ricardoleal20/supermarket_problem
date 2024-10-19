"""
Optimized file that runs the app for local or production deployment.
"""
from typing import Any
import os
import asyncio
import signal
import uvicorn
# FastAPI import
from fastapi import FastAPI


class Server:
    """
    Class to manage the Uvicorn server for production deployments.
    Args:
        app (Any): FastAPI app instance.
        host (str): The host to bind to.
        port (int): The port to bind to.
        log_level (str): Log level for the server.
        reload (bool): Enable auto-reload (for development environments).
    """
    _url: str

    def __init__(self,
                 app: FastAPI,
                 host: str = os.getenv("HOST", "localhost"),
                 port: int = int(os.getenv("PORT", 3000)),
                 log_level: str = os.getenv("LOG_LEVEL", "info"),
                 reload: bool = False) -> None:
        # Define the url
        self._url = f"http://{host}:{port}"
        # Uvicorn server configuration
        self.config = uvicorn.Config(
            app=app,
            host=host,
            port=port,
            log_level=log_level,
            reload=reload,
        )
        self.server = uvicorn.Server(self.config)

    async def start(self) -> None:
        """Start the Uvicorn server asynchronously."""
        print("Starting server...")
        print(" "+10*"="+"APP INFO"+10*"=")
        print(" |"+f"Running on: {self._url}")
        print(" "+28*"=")
        await self.server.serve()

    def stop(self) -> None:
        """Gracefully stop the server."""
        print("Shutting down server...")
        self.server.should_exit = True


def handle_shutdown(loop: asyncio.AbstractEventLoop, server: Server) -> None:
    """Handles shutdown signals to gracefully stop the server."""
    print("Received shutdown signal. Closing the server...")
    server.stop()
    loop.stop()


async def keep_running() -> None:
    """Optional task to keep the server alive, logging status periodically."""
    while True:
        await asyncio.sleep(60)
        print("Server keep running...")


def run_server(api_to_run: Any) -> None:
    """
    Run the server.
    Args:
        api_to_run (Any): The FastAPI app class to run.
    """
    # Create server instance
    server = Server(app=api_to_run)
    loop = asyncio.get_event_loop()

    # Register shutdown handlers for production
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: handle_shutdown(loop, server))

    try:
        # Run the server and ensure background tasks if needed
        loop.create_task(server.start())
        loop.create_task(keep_running())  # Optional: Remove if not needed
        loop.run_forever()
    except KeyboardInterrupt:
        print("Keyboard interrupt received. Shutting down...")
    finally:
        loop.close()
