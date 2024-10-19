"""
Provide a Base API to use on the server handler
"""
from fastapi import FastAPI, HTTPException
# Import also the CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
# Local imports
from supermarket_implementation.__info__ import (
    APP_NAME, DESCRIPTION, contact, __version__, __license__
)


class App():  # pylint: disable=R0903
    """Application to handle the backend server for this problem

    - client (property): To return the client and be used in the `run_server`
    - allow_cors_middleware: To config a pre-determinate middleware
    """
    _app: FastAPI
    # Define the slots
    __slots__ = ["_app"]

    def __init__(self) -> None:
        """Simply initialize the application"""
        # Initialize the FastAPI object
        self._app = FastAPI(
            title=APP_NAME,
            description=DESCRIPTION,
            version=__version__,
            contact=contact,
            license_info=__license__
        )
        # **************************** #
        # *        Endpoints         * #
        # **************************** #
        self._app.get("/")(self.__default)
        self._app.get("/{unknown_pages}")(self.__404)

    def allow_cors_middleware(self) -> None:
        """Allow the cors middleware config"""
        self._app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"]
        )

    @property
    def client(self) -> FastAPI:
        """Method that only returns the FastAPI object

        Returns:
            FastAPI: FastAPI object
        """
        return self._app
    # -------------------- #
    #    DEFAULT PAGE      #
    # -------------------- #

    async def __default(self) -> dict:
        return {"message": "This is the default page. To see more options, please go to `/docs`"}

    # -------------------- #
    #   OTHER ENDPOINTS    #
    # -------------------- #
    async def __404(self) -> None:
        """Return the 404"""
        raise HTTPException(status_code=404, detail="Endpoint not found")
