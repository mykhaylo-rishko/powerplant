from pydantic import BaseModel, Field
from typing import List

class Fuels(BaseModel):
    gas_eur_per_mwh: float = Field(alias="gas(euro/MWh)")
    kerosine_eur_per_mwh: float = Field(alias="kerosine(euro/MWh)")
    co2_eur_per_ton: float = Field(alias="co2(euro/ton)")
    wind_percentage: float = Field(alias="wind(%)")

class Powerplant(BaseModel):
    name: str
    type: str
    efficiency: float
    pmin: int
    pmax: int

class Payload(BaseModel):
    load: int
    fuels: Fuels
    powerplants: List[Powerplant]

class ProductionPlanItem(BaseModel):
    name: str
    p: float
