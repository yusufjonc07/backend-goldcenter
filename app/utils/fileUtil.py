import os
import uuid
from anyio import Path
from fastapi import HTTPException, UploadFile
from app.schemas.enums import MediaTypes
from config import CONTENT_TYPES


async def validate_file(file: UploadFile, type: MediaTypes, maxSize: float):

    #checking type of the file uploading
    if not file.content_type in CONTENT_TYPES[type]:
        raise HTTPException(400, "Fayl formati noto'g'ri!")

    file_contents = await file.read()

    file.filename = f"{uuid.uuid4()[:10]}__{file.filename}"

    if len(file_contents) > maxSize * 1024 * 1024:
        raise HTTPException(
            400, f"Fayl kattaligi maksimal {maxSize} MB!")
    
    return

async def upload_file(file: UploadFile, url:Path):

    file_contents = await file.read()
    
    upload_dir = os.path.join(os.getcwd(), url)
    # Create the upload directory if it doesn't exist
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # get the destination path
    dest = os.path.join(upload_dir, file.filename)

    with open(f"assets/employeeAgreements/{file_contents.filename}", "wb") as f:
                f.write(file_contents)