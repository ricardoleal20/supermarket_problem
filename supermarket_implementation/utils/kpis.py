"""
Methods to calculate the KPIs to send to the front end
"""
from supermarket_implementation.models import SolutionVar


def calculate_service_time_kpi(data: list[SolutionVar]) -> float:
    """Calculate the service time KPI.
    
    This time would be calculated as the average time a client spends in the
    queue until it gets out (using also the processing time)
    """
    # First, get the average sum of each client since they have arrival to the
    # queue until they leave the cashier
    total_service_time = sum(d.end - d.client.arrival_time for d in data)
    # From there, just divide by the number of clients and return it
    return round(total_service_time / len(data), 1)


def calculate_waiting_time_kpi(data: list[SolutionVar]) -> float:
    """Calculate the waiting time KPI.

    This time would be calculated as the average time a client spends in the
    queue until it gets to the cashier
    """
    # First, get the average sum of each client from the arrival time to the
    # beginning of the service
    total_service_time = sum(d.start - d.client.arrival_time for d in data)
    # From there, just divide by the number of clients and return it
    return round(total_service_time / len(data), 1)


def calculate_cashier_free_time_kpi(data: list[SolutionVar]) -> float:
    """Calculate the cashier free time KPI.

    This time would be calculated as the average time a cashier spends without
    attending a client
    """
    # First, consider the total range of time of the simulation.
    total_time = max(d.end for d in data)
    # Then, get the total time that each cashier has been working
    total_working_time = sum(d.end - d.start for d in data)
    # Then, to get the average free time that the cashiers have, just divide
    # the total working time by the total time
    return round(total_working_time / total_time, 1)


def calculate_service_level_kpi(data: list[SolutionVar]) -> float:
    """Calculate the service level KPI.

    This time would be calculatd considering:
        - The clients that have be attendend in the first 3 minutes since they arrive to the queue
        - The total number of clients
    """
    # Get first the clients that have been attended in the first 3 minutes
    attended_clients = sum(
        1 for d in data if d.start -
        d.client.arrival_time <= 3
    )
    # Return the calculation
    return round(attended_clients / len(data), 1)
