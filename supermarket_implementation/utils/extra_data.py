"""
Code to calculate the performance individually of each cashier
"""
from typing_extensions import TypedDict
# External imports
import pydash as _py
# Local imports
from supermarket_implementation.utils import kpis as KPI
from supermarket_implementation.models import SolutionVar


class IndividualCashierPerformance(TypedDict):
    """Cashier Performance KPIs"""
    workerId: str
    serviceLevel: float
    avgQueueWaitingTime: float
    avgProcessingTime: float
    avgFreeTime: float


class CashiersPerformance(TypedDict):
    """Cashiers Performance KPIs"""
    morning: list[IndividualCashierPerformance]
    afternoon: list[IndividualCashierPerformance]


class EfficiencyData(TypedDict):
    """Efficiency data for each shift"""
    id: str
    label: str
    value: float

class ClientPerProduct(TypedDict):
    """Clients per product"""
    # dataKey: str
    label: str
    data: list[float]


class ArrivalVsStart(TypedDict):
    """Arrival vs Start data"""
    x: int
    y: int


class ScatterData(TypedDict):
    """Scatter Data graph for the arrival vs the start"""
    label: str
    data: list[ArrivalVsStart]


def calculate_cashier_performance(
        data: list[SolutionVar]
) -> CashiersPerformance:
    """Calculate the performance by cashier. This calculation will be done individually
    for each cashier that we have on the data.
    """
    performance_per_cashier: CashiersPerformance = {
        "morning": [], "afternoon": []
    }
    # Group the data for their shift
    data_per_shift = _py.group_by(
        data, lambda x: "morning" if x.start <= 360 else "afternoon")
    for shift, shift_data in data_per_shift.items():
        # Then, group the data for each cashier
        data_per_cashier = _py.group_by(shift_data, lambda x: x.cashier.name)
        # Calculate the performance for this cashier
        performance_per_cashier[shift] = [
            {
                "workerId": worker_id,
                "serviceLevel": KPI.calculate_service_level_kpi(cashier_data),
                "avgQueueWaitingTime": KPI.calculate_service_time_kpi(cashier_data),
                "avgProcessingTime": KPI.calculate_waiting_time_kpi(cashier_data),
                "avgFreeTime": KPI.calculate_cashier_free_time_kpi(cashier_data)
            }
            for worker_id, cashier_data in data_per_cashier.items()
        ]
    # At the end, return the KPI per cashier
    return performance_per_cashier


def get_clients_per_product(data: list[SolutionVar]) -> list[ClientPerProduct]:
    """Get the clients divided by their product section"""
    def section_per_data(value: int) -> str:
        """Return which section is the value"""
        if value < 15:
            return "<15 products"
        if 15 <= value < 30:
            return "15-30 products"
        return ">30 products"

    final_data: list[ClientPerProduct] = [
        {"label": "Morning", "data": []},
        {"label": "Afternoon", "data": []}
    ]

    # First, get the data per section
    data_per_section = _py.group_by(
        data, lambda x: section_per_data(x.client.products)
    )
    # Sort the data per data per section by the key. First the <15, then 15-30 and finally >30
    data_per_section = {
        "<15 products": data_per_section.get("<15 products", []),
        "15-30 products": data_per_section.get("15-30 products", []),
        ">30 products": data_per_section.get(">30 products", [])
    }
    # Then, from it, get the data per section
    for section_data in data_per_section.values():
        data_per_shift = _py.group_by(
            section_data, lambda x: "morning" if x.start <= 360 else "afternoon")
        if "morning" not in data_per_shift:
            data_per_shift["morning"] = []
        # For each shift, set the data
        for shift, shift_data in data_per_shift.items():
            # Get the index depending on the shift
            index = 0 if shift == "morning" else 1
            if not shift_data:
                final_data[index]["data"].append(0)
                continue
            # Get the waiting time for this
            final_data[index]["data"].append(
                round(sum(x.duration for x in shift_data) / len(shift_data), 2)
            )
    # Then, just return the data
    return final_data


def get_scatter_data(data: list[SolutionVar]) -> list[ScatterData]:
    """Get the scatter data for the arrival vs the start"""
    scatter_data: ScatterData = {
        "label": "Arrival vs Start",
        "data": []
    }
    for var in data:
        scatter_data["data"].append({
            "x": var.client.arrival_time,
            "y": var.start
        })
    return [scatter_data]


def get_shift_efficiency(data: list[SolutionVar]) -> list[EfficiencyData]:
    """Get the shift efficiency considering all the KPIs for each one of the shifts
    
    Based on each shift, we'll consider the KPIs for that shift and we'll see how much
    efficient is that shift based on the other shift. The ideal scenario would be that
    both shifts have 50% and 50% of the efficiency, but it's not always the case.

    In this case, the one with higher efficiency would be the best one equipped.
    """
    efficiency_data: list[EfficiencyData] = []
    # Group the data per shift
    data_per_shift = _py.group_by(
        data, lambda x: "morning" if x.start <= 360 else "afternoon")
    for shift, shift_data in data_per_shift.items():
        # Calculate the KPIs for this shift
        service_level = KPI.calculate_service_level_kpi(shift_data)
        avg_queue_waiting_time = KPI.calculate_service_time_kpi(shift_data)
        avg_processing_time = KPI.calculate_waiting_time_kpi(shift_data)
        avg_free_time = KPI.calculate_cashier_free_time_kpi(shift_data)
        # Calculate the efficiency for this shift
        efficiency = round((
            service_level + avg_queue_waiting_time +
            avg_processing_time + avg_free_time
        ) / 4, 2)
        efficiency_data.append({
            "id": shift,
            "label": f"{shift.capitalize()} Shift",
            "value": efficiency
        })

    # Calculate the total efficiency of the day
    total_efficiency = sum(item["value"] for item in efficiency_data)
    # Normalize the efficiency to make the sum 100%
    for item in efficiency_data:
        item["value"] = round((item["value"] / total_efficiency) * 100, 2)
    # Then, just return the data
    return efficiency_data
