"""
Provide a Base API to use on the server handler
"""
from typing_extensions import TypedDict
from fastapi import FastAPI, HTTPException
# Import also the CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# Local imports
from supermarket_implementation.scheduling import CashierScheduling
from supermarket_implementation.models import Cashier, Client
from supermarket_implementation.utils import kpis as KPI
from supermarket_implementation.utils.extra_data import (
    # CashiersPerformance, calculate_cashier_performance,
    ClientPerProduct, get_clients_per_product,
    ScatterData, get_scatter_data,
    EfficiencyData, get_shift_efficiency
)
from supermarket_implementation.__info__ import (
    APP_NAME, DESCRIPTION, contact, __version__, __license__
)

# Define some types


class CashierDict(TypedDict):
    """Client dictionary"""
    workerId: str
    available_in_the_morning: bool
    available_in_the_afternoon: bool
    effectiveness_average: float

# Define the ClientRequest class

class ClientRequest(BaseModel):
    """Client Request for the POST method"""
    morning_variance: float
    afternoon_variance: float


class SolverRequest(BaseModel):
    """Solver Request for the POST method"""
    cashiers: list[CashierDict]
    clients: list[dict[str, int]]


class SolverResult(BaseModel):
    """Solver Result to result from the POST method"""
    ganttSolution: list[dict]
    # cashierPerformance: CashiersPerformance
    arrivalVsStart: list[ScatterData]
    clientPerProducts: list[ClientPerProduct]
    efficiencyData: list[EfficiencyData]
    serviceLevel: float
    avgQueueWaitingTime: float
    avgProcessingTime: float
    avgFreeTime: float

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
        self._app.post("/solve_problem")(self.execute_solver)
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
        return {
            "message": "This is the default page for the API." +
            " To see more options, please go to `/docs`"
        }

    # -------------------- #
    #   OTHER ENDPOINTS    #
    # -------------------- #

    async def execute_solver(self, request: SolverRequest) -> SolverResult:
        """Execute the solver"""
        print(
            f"Executing the solver with {len(request.clients)}" +
            f" clients and {len(request.cashiers)} cashiers"
        )
        # Instance th solver result
        solution = []
        # Obtain the cashiers and clients model
        cashiers = [
            Cashier(
                name=cashier["workerId"],
                available_in_the_morning=cashier["available_in_the_afternoon"],
                available_in_the_afternoon=cashier["available_in_the_afternoon"],
                effectiveness_average=cashier["effectiveness_average"],
            )
            for cashier in request.cashiers
        ]
        clients = [
            Client(
                id=client["id"],
                arrival_time=client["arrivalTime"],
                products=client["products"]
            )
            for client in request.clients
        ]
        # Set the cashiers
        self._solver.set_cashiers(cashiers)
        self._solver.set_clients(clients)
        # Then, solve the problem
        self._solver.solve()
        # Get the solver
        solver = self._solver.solver
        # Get the results
        try:
            results = self._solver.results()
        except Exception as e:
            print(f"Solver failed with error: {e}")
            raise HTTPException(
                status_code=500, detail="Solver failed to find a solution") from e
        # Get the solver result
        print("Modifyng the results...")
        solution = [{
            "id": f"TASK_{var.client.id}_{var.cashier.name}",
            "processor": var.cashier.name,
            "task": f"Client {var.client.id}",
            "start": solver.Value(var.start),
            "end": solver.Value(var.end),
            "duration": var.duration,
            "products": var.client.products
        } for var in results]
        # Return the SolverResult
        print("Sending the results...")
        return SolverResult(
            avgProcessingTime=KPI.calculate_service_time_kpi(results),
            avgQueueWaitingTime=KPI.calculate_waiting_time_kpi(results),
            avgFreeTime=KPI.calculate_cashier_free_time_kpi(results),
            serviceLevel=KPI.calculate_service_level_kpi(results),
            # cashierPerformance=calculate_cashier_performance(results),
            clientPerProducts=get_clients_per_product(results),
            arrivalVsStart=get_scatter_data(results),
            efficiencyData=get_shift_efficiency(results),
            ganttSolution=solution
        )

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
