"""
Provide a Base API to use on the server handler
"""
from fastapi import FastAPI, HTTPException
# Import also the CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# Local imports
from supermarket_implementation.scheduling import CashierScheduling
from supermarket_implementation.__info__ import (
    APP_NAME, DESCRIPTION, contact, __version__, __license__
)

# Define the ClientRequest class


class ClientRequest(BaseModel):
    """Client Request for the POST method"""
    morning_variance: float
    afternoon_variance: float

class App():  # pylint: disable=R0903
    """Application to handle the backend server for this problem

    - client (property): To return the client and be used in the `run_server`
    - allow_cors_middleware: To config a pre-determinate middleware
    """
    _app: FastAPI
    _solver: CashierScheduling
    # Define the slots
    __slots__ = ["_app", "_solver"]

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
        # Initialize the scheduling problem
        self._solver = CashierScheduling()
        # **************************** #
        # *        Endpoints         * #
        # **************************** #
        self._app.get("/")(self.__default)
        self._app.post("/generate_clients")(self.generate_clients)
        self._app.get("/{unknown_pages}")(self.__404)

        # * Add the middleware
        self.allow_cors_middleware()

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
        return {"message": "This is the default page for the API. To see more options, please go to `/docs`"}

    # -------------------- #
    #   OTHER ENDPOINTS    #
    # -------------------- #

    # Reemplaza el $SELECTION_PLACEHOLDER$ con el siguiente código
    async def generate_clients(
        self,
        request: ClientRequest
    ) -> list[dict]:
        """Generate the clients using the solver with given variances"""
        print("Generating clients for this run...")
        return [
            client.to_dict()
            for client in self._solver.generate_clients(
                request.morning_variance,
                request.afternoon_variance
            )
        ]

    async def __404(self) -> None:
        """Return the 404"""
        raise HTTPException(status_code=404, detail="Endpoint not found")
