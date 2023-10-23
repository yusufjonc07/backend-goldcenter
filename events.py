from fastapi_utils.tasks import repeat_every
from fastapi import APIRouter
import subprocess
import random
import string

events_router = APIRouter()

@events_router.on_event("startup")
@repeat_every(seconds=10, wait_first=True)
async def auto_committer():

    try:
        with open("./data.txt", "w") as f:
            longText = ''.join(random.choices(string.ascii_lowercase, k=1000))
            longTextArr = longText.split('a')
            f.write(" \n".join(longTextArr))
            f.close()

        commitText = ''.join(random.choices(string.ascii_lowercase, k=8))
        res = subprocess.run(f"git add data.txt; git commit -m'{commitText}'; git push", capture_output=True, shell=True)
        print(res.stdout.decode())

    except Exception as e:
        print(e.args)
