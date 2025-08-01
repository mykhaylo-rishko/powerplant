from .models import Payload, ProductionPlanItem

def calculate_production_plan(payload: Payload) -> list[ProductionPlanItem]:
    powerplants = payload.powerplants
    fuels = payload.fuels
    load = payload.load
    
    merit_order = []

    for plant in powerplants:
        cost = 0.0

        if plant.type == "windturbine":
            cost = 0
            p_available = plant.pmax * (fuels.wind_percentage / 100)
        
        elif plant.type == "gasfired":
            cost = fuels.gas_eur_per_mwh / plant.efficiency
            p_available = plant.pmax

        elif plant.type == "turbojet":
            cost = fuels.kerosine_eur_per_mwh / plant.efficiency
            p_available = plant.pmax
            
        else:
            continue
            
        merit_order.append({
            "name": plant.name,
            "type": plant.type,
            "cost": cost,
            "pmin": plant.pmin,
            "pmax": plant.pmax,
            "p_available": p_available,
            "p_assigned": 0.0
        })

    #Ordenar
    merit_order.sort(key=lambda p: p["cost"])
    
    remaining_load = float(load)
    
    for plant in merit_order:
        if plant["type"] == "windturbine":
            power_to_assign = plant["p_available"]
            plant["p_assigned"] = power_to_assign
            remaining_load -= power_to_assign
            

    for plant in merit_order:
        if plant["type"] in ["gasfired", "turbojet"]:
            if remaining_load <= 0:
                break
            
            if remaining_load >= plant["pmin"]:
                power_to_assign = min(plant["p_available"], remaining_load)
                
                plant["p_assigned"] = power_to_assign
                remaining_load -= power_to_assign

    current_total_production = sum(p["p_assigned"] for p in merit_order)
    diff = load - current_total_production

    if abs(diff) > 0.01:
        for plant in sorted(merit_order, key=lambda p: p["cost"], reverse=True):
            if plant["p_assigned"] > 0 and plant["type"] != "windturbine":
                if plant["p_assigned"] + diff <= plant["pmax"]:
                    plant["p_assigned"] += diff
                    break

   
    response = []
    for plant in payload.powerplants: 
        assigned_power = 0.0
        for p_merit in merit_order:
            if p_merit["name"] == plant.name:
                assigned_power = round(p_merit["p_assigned"], 1)
                break
        response.append(ProductionPlanItem(name=plant.name, p=assigned_power))
        
    return response