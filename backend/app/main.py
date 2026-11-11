from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.rest import router as rest_router
from app.api.openai import openai_router
from app.api.mcp import mcp_server
from app.db.database import Base, engine, SessionLocal
from app.models.catalog import ModelRegistry

Base.metadata.create_all(bind=engine)
with SessionLocal() as db:
    ModelRegistry.seed_defaults(db)

app = FastAPI(
    title="Voice AI Studio API",
    description="Enterprise Local AI Engine Platform for Voice Synthesis, Cloning, STT, Dubbing and Audiobooks",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rest_router)
app.include_router(openai_router)

@app.get("/")
def root():
    return {"status": "online", "system": "Voice AI Studio API", "version": "1.0.0"}

@app.get("/mcp/tools")
def mcp_tools():
    return {"tools": mcp_server.get_tools()}

@app.post("/mcp/call")
def mcp_call(payload: dict):
    tool_name = payload.get("name")
    arguments = payload.get("arguments", {})
    return mcp_server.call_tool(tool_name, arguments)
