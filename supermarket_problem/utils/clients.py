"""
Add extra utilities for the clients, such as a client generator based on the
poisson distribution
"""
import typing as tp
# External imports
import numpy as np
# Local imports
from supermarket_problem.models import Client


def generate_clients_based_on_poisson(
    morning_variance: float,
    afternoon_variance: float
) -> list[Client]:
    """Generate the clients based on a Poisson distribution.
    
    We just define a poisson parameter for the morning schedule
    and one for the afternoon schedule, and with that, we can generate
    the clients for this run.
    """
    id_gen = __id_generator()
    # Start creating the clients list
    clients = __clients_per_shift(morning_variance, id_gen)
    # Then, add the clients for the afternoon shift
    clients.extend(__clients_per_shift(afternoon_variance, id_gen, True))
    # And return it at the end
    return clients

# ========================= #
#      Helper methods       #
# ========================= #


def __clients_per_shift(
    variance: float,
    id_generator: tp.Generator[int, None, None],
    afternoon: bool = False
) -> list[Client]:
    """Generate clients per shift. Using the variance to know how many
    clients we're going to get per shift. Using the afternoon flag would change
    the time from (0, 360) to (360, 720)
    """
    time_range = (0, 360) if afternoon is False else (360, 720)
    # Generate the amount of clients to arrive
    return [
        Client(
            id=next(id_generator),
            arrival_time=np.random.randint(*time_range),
            products=np.random.randint(1, 50)
        )
        for _ in range(np.random.poisson(variance))
    ]


def __id_generator() -> tp.Generator[int, None, None]:
    """Generate an ID for the method"""
    current_id = 0
    while True:
        yield current_id
        # Then, update the ID
        current_id += 1
