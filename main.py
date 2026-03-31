from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from mytypes import *
import numpy as np
import uvicorn
from fastapi.staticfiles import StaticFiles
from SmartTiming.api import router as smarttiming_router
from test.testapi import router as testapi_router
from settings import settings
import os


app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.include_router(smarttiming_router)
#app.include_router(testapi_router)  
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.post("/CriticalPower", response_model=CriticalPowerResultModel) 
def CriticalPower(
    data: PointsModel
): 

    # get data & invert x
    x = np.array([1.0/p.x for p in data.points]) 
    y = np.array([p.y for p in data.points]) 

    # linear regression
    W, CP = np.polyfit(x, y, 1)
    
    return CriticalPowerResultModel(CP=CP, W=W)


if __name__ == "__main__":
    os.environ["ENVIRONMENT"] = "development"
    uvicorn.run(app, host="0.0.0.0", port=8002)
    