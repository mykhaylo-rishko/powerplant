import uvicorn
from fastapi import FastAPI, HTTPException
from typing import List

from app.models import Payload, ProductionPlanItem
from app.repository import calculate_production_plan

app = FastAPI(
    title="Powerplant TMC",
)

@app.post("/productionplan", response_model=List[ProductionPlanItem])
async def create_production_plan_endpoint(payload: Payload):
    try:
        production_plan = calculate_production_plan(payload)
        return production_plan
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, 
            detail="ERROR"
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)