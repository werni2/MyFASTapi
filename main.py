from fastapi import FastAPI
from mytypes import *
import numpy as np
import uvicorn
from SmartTiming.api import router as smart_router
from testapi import router as testapi_router

app = FastAPI()
app.include_router(smart_router)
app.include_router(testapi_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)
    