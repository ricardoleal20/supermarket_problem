"""
Problem utilities
"""
import pydash as _py
# OR Tools import
from ortools.sat.python import cp_model
# Local imports
from supermarket_implementation.models import (
    Client, Cashier, SolverVar
)

AVG_PROCESS_TIME_PER_ITEM = 0.25  # minutes


def ignite_variables(
    clients: list[Client],
    cashiers: list[Cashier],
    model: cp_model.CpModel
) -> list[SolverVar]:
    """Ignitie the variables to use to solve the optimization problem"""
    # Create the array of solution vars
    solutions: list[SolverVar] = []
    for cashier in cashiers:
        for client in clients:
            if client.arrival_time <= 360 and cashier.available_in_the_morning is False:
                continue
            if client.arrival_time > 360 and cashier.available_in_the_afternoon is False:
                continue
            solutions.append(SolverVar(
                cashier=cashier,
                client=client,
                start=model.NewIntVar(
                    client.arrival_time, 720,
                    f"START_{cashier.name}_T{client.id}"
                ),
                end=model.NewIntVar(
                    client.arrival_time, 720,
                    f"END_{cashier.name}_T{client.id}"
                ),
                duration=__calculate_expected_duration(client, cashier),
                active=model.NewBoolVar(f"ACTIVE_{cashier.name}_T{client.id}")
            ))
    return solutions


def ignite_constraints(
    solution_vars: list[SolverVar],
    model: cp_model.CpModel
) -> None:
    """Ignite the constraints, such as:
        - The end should be: end == start + duration
        - Only one client per cashier
        - Only 1 active var per client
    """
    intervals_per_cashier = {}
    for var in solution_vars:
        # Add the 1st restriction. End == start + duration.
        # * Note: Remember to only enforce this situation if
        # * the var is active.
        model.Add(var.end == var.start +
                  var.duration).OnlyEnforceIf(var.active)
        # Create a duration var
        duration_var = model.NewIntVar(
            0, var.duration,
            f"DURATION_{var.cashier.name}->T{var.client.id}"
        )
        # Add the interval
        if var.cashier.name not in intervals_per_cashier:
            intervals_per_cashier[var.cashier.name] = []
        # Then, add an interval
        intervals_per_cashier[var.cashier.name].append(model.NewOptionalIntervalVar(
            var.start, duration_var, var.end, var.active,
            f"INTERVAL_{var.cashier.name}->T{var.client.id}"
        ))

    # Then, add the second restriction. Only one client per cashier
    for intervals in intervals_per_cashier.values():
        model.AddNoOverlap(intervals)

    # Then, add the third restriction. Only one active per client
    vars_per_client = _py.group_by(solution_vars, lambda x: x.client.id)
    for variables in vars_per_client.values():
        model.AddExactlyOne((v.active for v in variables))


def ignite_objectives(
    solution_vars: list[SolverVar],
    model: cp_model.CpModel
) -> None:
    """Ignite the objectives of the optimization model
    
    In theo objectives, we have:
        - makespan: The general makespan of the entire model
        - process_time: How much process time does it takes to attend all the clients
        - clients_waiting_time: The time that each client is waiting to start in the line
    """
    objective_var = model.NewIntVar(0, int(1e6), "OBJECTIVE_SUM")

    # First of all, ignite the makespan
    makespan = model.NewIntVar(0, int(1e6), "makespan")
    model.AddMaxEquality(makespan, [v.end for v in solution_vars])
    # Then, ignite the process time of each client
    process_time = model.NewIntVar(0, int(1e6), "process_time")
    model.Add(process_time == sum(v.end - v.start for v in solution_vars))
    # Now, ignite the waiting time on the line for each var
    clients_waiting_time = model.NewIntVar(0, int(1e6), "clients_waiting_time")
    model.Add(clients_waiting_time == sum(
        v.start - v.client.arrival_time for v in solution_vars))

    # Add the values for the objective var. Sum all the variables
    model.Add(objective_var == makespan + process_time + clients_waiting_time)
    # Minimize the objective sum
    model.Minimize(objective_var)


# ========================== #
#        Helper methods      #
# ========================== #


def __calculate_expected_duration(client: Client, cashier: Cashier) -> int:
    """Calculate the duration of a client and a cashier"""
    return int(
        client.products * (
            AVG_PROCESS_TIME_PER_ITEM
            / cashier.effectiveness_average
        )
    )
