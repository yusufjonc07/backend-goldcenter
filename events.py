import subprocess
from fastapi.responses import PlainTextResponse, StreamingResponse, FileResponse
from fastapi_utils.tasks import repeat_every
from fastapi import APIRouter
import random
import string
from app.utils.wsmanager import manager


events_router = APIRouter()


@events_router.on_event("startup")
async def auto_committer():
    manager.active_connections = []
