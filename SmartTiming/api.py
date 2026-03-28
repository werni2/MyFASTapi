from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from fastapi.responses import JSONResponse
from SmartTiming.sessionstore import *
 
router = APIRouter()
session_store = InMemorySessionStore()  # globale Instanz

def get_session_store():
    return session_store
    
@router.post("/CreateTimingSession")
async def create_timing_session(
    session_name: str,
    store = Depends(get_session_store)
):
    if not session_name.strip():
        return JSONResponse(
            status_code=500,
            content={
                "error": "session_name darf nicht leer sein"
            }
        )

    try:
        await store.create(session_name)

    except Exception as ex:
        return JSONResponse(
            status_code=500,
            content={
                "error": str(ex)
            }
        )
    
    return JSONResponse(
        status_code=200,
        content={
            "session_name": session_name
        }
    )

@router.get("/session_ids")
async def list_session_ids(store = Depends(get_session_store)):
    session_ids = await store.session_ids()
    return JSONResponse(
        status_code=200,
        content=session_ids
    )