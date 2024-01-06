import subprocess
from fastapi.responses import PlainTextResponse, StreamingResponse, FileResponse
from fastapi_utils.tasks import repeat_every
from fastapi import APIRouter
import random
import string
from app.utils.wsmanager import manager

events_router = APIRouter()


@events_router.on_event("startup")
@repeat_every(seconds=300, wait_first=True)
async def auto_committer():

    manager.active_connections = []

    try:
        with open("./data.txt", "w") as f:
            longText = ''.join(random.choices(string.ascii_lowercase, k=1000))
            longTextArr = longText.split('a')
            f.write(" \n".join(longTextArr))
            f.close()

    except Exception as e:
        print(e.args)
