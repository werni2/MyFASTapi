from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import JSONResponse, HTMLResponse
from SmartTiming.sessionstore import *
from fastapi.templating import Jinja2Templates
from settings import settings
from mytypes import *
 
router = APIRouter()

# Globale Instanz des SessionStores (InMemory)
# Dadurch bleiben Sessions während der Laufzeit erhalten.
session_store = InMemorySessionStore()

# Jinja2 Template Engine für HTML-Rendering
templates = Jinja2Templates(directory="templates")


def get_session_store():
    """
    Dependency-Funktion, die den globalen SessionStore zurückgibt.
    Wird von FastAPI automatisch in Endpoints injiziert.
    """
    return session_store


# ---------------------------------------------------------
# Session erstellen
# ---------------------------------------------------------
@router.post("/timing_sessions")
async def create_timing_session(
    body: SessionCreate,
    store = Depends(get_session_store)
):
    """
    Erstellt eine neue Timing-Session.
    - session_name: Name der Session, muss nicht leer sein.
    - store: InMemorySessionStore (via Dependency Injection)
    """

    session_name = body.session_name

    # Validierung
    if not session_name.strip():
        return JSONResponse(
            status_code=500,
            content={"error": "session_name darf nicht leer sein"}
        )

    try:
        # Session im Store anlegen (async)
        await store.create(session_name)

    except Exception as ex:
        # Fehler beim Erstellen der Session
        return JSONResponse(
            status_code=500,
            content={"error": str(ex)}
        )
    
    # Erfolgreiche Antwort
    return JSONResponse(
        status_code=200,
        content={"session_name": session_name}
    )


# ---------------------------------------------------------
# Liste aller Session-IDs abrufen
# ---------------------------------------------------------
@router.get("/timing_sessions")
async def list_session_ids(store = Depends(get_session_store)):
    """
    Gibt eine Liste aller existierenden Session-Namen zurück.
    """
    session_ids = await store.session_ids()

    return JSONResponse(
        status_code=200,
        content=session_ids
    )


# ---------------------------------------------------------
# Client tritt einer Session bei
# ---------------------------------------------------------
@router.post("/timing_sessions/{session_id}/clients")
async def join_timing_session(
    session_id: str,
    body: JoinSessionRequest,
    store = Depends(get_session_store)
):
    client_name = body.client_name

    # Validierung
    if not session_id.strip():
        return JSONResponse(
            status_code=500,
            content={"error": "session_name darf nicht leer sein"}
        )
     
    if not client_name.strip():
        return JSONResponse(
            status_code=500,
            content={"error": "client_name darf nicht leer sein"}
        )
    
    try:
        # Session abrufen
        session = await store.get(session_id)

        # Client hinzufügen (async)
        await session.add_client(client_name)

    except Exception as ex:
        # Fehler beim Hinzufügen
        return JSONResponse(
            status_code=500,
            content={"error": str(ex)}
        )
     
    # Erfolgreiche Antwort
    return JSONResponse(
        status_code=200,
        content=f"Client {client_name} zur Session {session_id} hinzugefügt"
    )

# ---------------------------------------------------------
# Liste aller Clients einer Session abrufen
# ---------------------------------------------------------
@router.get("/timing_sessions/{session_id}/clients", response_model=List[TimingClientStateModel])
async def get_timing_clients(
    session_id: str,
    store = Depends(get_session_store)
):
    try:
        # Session abrufen
        session = await store.get(session_id)

        # Clients abrufen
        clients = await session.get_all_clients()

        return [TimingClientStateModel(
            client_id=c.client_id,
            latitude=c.latitude,
            longitude=c.longitude,
            speed=c.speed
        ) for c in clients]

    except Exception as ex:
        return JSONResponse(
            status_code=500,
            content={"error": str(ex)}
        )
    
# ---------------------------------------------------------
# Client updaten
# ---------------------------------------------------------
@router.patch("/timing_sessions/{session_id}/client/{client_id}", response_model=TimingClientStateModel)
async def update_timing_clients(
    session_id: str,
    client_id: str,
    update_data: UpdateClientRequest,
    store = Depends(get_session_store)
):
    try:
        # Session abrufen
        session = await store.get(session_id)

        # Clients abrufen
        client = await session.get_client(client_id)

        # Update den Client
        client.update(update_data)

        # Gibt das aktualisierte Client-Modell zurück
        return TimingClientStateModel(
            client_id=client.client_id,
            latitude=client.latitude,
            longitude=client.longitude,
            speed=client.speed
        )

    except Exception as ex:
        return JSONResponse(
            status_code=500,
            content={"error": str(ex)}
        )


# ---------------------------------------------------------
# HTML-Clientseite ausliefern
# ---------------------------------------------------------
@router.get("/TimingClient", response_class=HTMLResponse)
async def get_client(request: Request):
    """
    Rendert die HTML-Seite für den Timing-Client.
    Übergibt zusätzlich:
    - request: für Jinja2 erforderlich
    - title: Seitentitel
    - utils_base_url: aus settings
    """
    return templates.TemplateResponse(
        "client.html",
        {
            "request": request,
            "title": "Meine Webseite",
            "utils_base_url": settings.utils_base_url
        }
    )
