"""
Main implementation of the problem for the super market issue
"""
# OR Tools import
from ortools.sat.python import cp_model
# Local imports
from supermarket_implementation.models import (
    Cashier, Client, SolverVar, SolutionVar
)
from supermarket_implementation.utils import clients as client_utils
from supermarket_implementation.utils import problem as problem_utils


class CashierScheduling:
    """Implement a class that schedules
    the assignation of clients to different cashiers.

    <ADD_MORE>
    """
    _cashiers: list[Cashier]
    _clients: list[Client]
    _solution: list[SolverVar]
    _model: cp_model.CpModel
    solver: cp_model.CpSolver
    # Define the slots for this class
    __slots__ = [
        "_cashiers", "_clients", "_solution",
        "_model", "solver"
    ]

    def __init__(self) -> None:
        self._cashiers = []
        self._clients = []
        self._solution = []
        # Create the model
        self._model = cp_model.CpModel()
        self.solver = cp_model.CpSolver()

    def set_cashiers(self, cashiers: list[Cashier]) -> None:
        """Set the cashiers that are available to be in the work schedule for the day"""
        self._cashiers = cashiers

    def set_clients(self, clients: list[Client]) -> None:
        """Set the cashiers that are available to be in the work schedule for the day"""
        self._clients = clients

    def generate_clients(self, morning_variance: float, afternoon_variance: float) -> list[Client]:
        """Generate the possible clients that are going to attend to the
        supermarket in this day.
        """
        # * NOTE: We use this method for two things:
        # *  - 1) To append the clients to the class
        # *  - 2) We'll add extra methods such to generate the clients
        self._clients = client_utils.generate_clients_based_on_poisson(
            morning_variance, afternoon_variance
        )
        # Based on this, set the clients
        return self._clients

    def solve(self) -> None:
        """Solve the problem.

        Using a different group of possible solutions (such as the queue model)
        would help us to define a better solution of the model
        """
        # Evaluate if we have clients and cashiers
        if not self._cashiers:
            raise Warning("There is no cashiers to use in this problem." +
                          " Append some using the method `set_cashiers`")
        if not self._clients:
            raise Warning("There is no clients to attend to the supermarket." +
                          " Generate some using the method `generate_clients`")

        # Then, generate the variables for the problem
        self._solution = problem_utils.ignite_variables(
            self._clients, self._cashiers, self._model)
        # Ignite the constraints and the objectives
        problem_utils.ignite_constraints(self._solution, self._model)
        problem_utils.ignite_objectives(self._solution, self._model)
        # At the end, just run the optimization!
        status = self.solver.Solve(self._model)

        if status not in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            raise RuntimeError("The problem cannot be solved...")
        # Otherwise, print that the solution has runned succesfully
        print("The problem has been solved succesfully in {} seconds!")

    def results(self, include_inactive: bool = False) -> list[SolutionVar]:
        """Once the scheduling has been made, return the vars that define the solution."""
        if not self._solution:
            raise Warning(
                "There's no solution available. Please run the `solve` method first.")
        # Convert the solver var to solution vars
        solutions_vars = [
            SolutionVar(
                cashier=var.cashier,
                client=var.client,
                start=self.solver.Value(var.start),
                end=self.solver.Value(var.end),
                duration=var.duration,
                active=self.solver.Value(var.active),
            )
            for var in self._solution
        ]
        # Return the solution. If we want to include the inactive too, then
        # return simply the reference to the solution
        if include_inactive is True:
            return solutions_vars
        # Otherwise, return the filtered solution. Convert each
        return [var for var in solutions_vars if var.active]
