import subprocess
from fastapi.responses import PlainTextResponse, StreamingResponse, FileResponse
from fastapi_utils.tasks import repeat_every
from fastapi import APIRouter
import random
import string

events_router = APIRouter()

@events_router.get("/backup")
async def backup_db():
    # Run mysqldump command to backup the database
    dump_cmd = [
        "mysqldump",
        f"--user=root",
        f"--password=I5yEdNFGoOiV4bB",
        f"--host=localhost",
        f"--port=3306",
        "--databases",
        f"goldcenter",
    ]
    dump_process = subprocess.Popen(dump_cmd, stdout=subprocess.PIPE)

    # Run mysql command to import the backup into the remote database
    import_cmd = [
        "mysql",
        f"--user=goldcenter",
        f"--password=goldcenter",
        f"--host=176.96.243.119",
        f"--port=3306",
        f"--database=goldcenter",
    ]
    
    import_process = subprocess.Popen(import_cmd, stdin=subprocess.PIPE)

    # Read and write data in chunks
    chunk_size = 4096
    while True:
        chunk = dump_process.stdout.read(chunk_size)
        if not chunk:
            break
        import_process.stdin.write(chunk)

    # Close stdin to signal the end of input
    import_process.stdin.close()

    # Wait for the import process to finish
    import_process.wait()

    # Stream the backup file as a response
    return PlainTextResponse('success')

@events_router.on_event("startup")
@repeat_every(seconds=300, wait_first=True)
async def auto_committer():

    try:
        with open("./data.txt", "w") as f:
            longText = ''.join(random.choices(string.ascii_lowercase, k=1000))
            longTextArr = longText.split('a')
            f.write(" \n".join(longTextArr))
            f.close()

    except Exception as e:
        print(e.args)
