"""
Models for the problem generation. This models would represent
a managable way to utilize the data around the general problem
"""
from dataclasses import dataclass
# Import or tools
from ortools.sat.python import cp_model


@dataclass
class Cashier:
    """Cashier representation model.

    Here, we include simple data as the name,
    the availability and their effectiveness range
    """
    name: str
    available_in_the_morning: bool
    available_in_the_afternoon: bool
    effectiveness_average: float

    def __repr__(self) -> str:
        return f"Cashier ID: {self.name}"


@dataclass
class Client:
    """Client representation model.
    
    Here, we can represent the id of arrival, the time of arrival
    to the queue and the quantity of products that they would like to buy.

    Since the supermarket is open from 8 am to 8 pm, we know that we
    have only 12 hours of usage in the supermarket. We allow the clients
    to arrive per minute, so it's easy to us to represent the client arrival time
    as an integer, telling us the minute that they arrive.

    For example, if the arrival time is 60, then we know that they arrive to the queue at
    9 am. If the arrival time is 172, then we know that they arrive at 10:52 am.
    """
    id: int
    arrival_time: int
    products: int

    def __repr__(self) -> str:
        return f"Client {self.id}, arriving at {self.arrival_date}" +\
            f" with {self.products} products to shop"

    @property
    def arrival_date(self) -> str:
        """Arrival date. It is just the representation of the hour
        and minute that this client arrives.
        """
        base_hour = 8
        hours = self.arrival_time // 60
        minutes = self.arrival_time % 60
        # Get the hour, depending on the base hour (8 am)
        hour = base_hour + hours
        return f"{hour:02}:{minutes:02}"


@dataclass
class SolutionVar:
    """Solution Var.
    This is more like a tuple of variables that represent one state of the solution.
    In this tuple of variables, we use:
        - cashier: The cashier that's gonna attend this client
        - client: Client to attend
        - start: At which time we're going to attend this client
        - end: At which time we finished of attending this client
        - active: This variable is on the final solution?
        - 

    """
    cashier: Cashier
    client: Client
    start: cp_model.IntVar
    end: cp_model.IntVar
    duration: int
    active: cp_model.BoolVarT

    def __repr__(self) -> str:
        return f"SolverVar::{self.cashier.name}|-->Active={self.active}"
