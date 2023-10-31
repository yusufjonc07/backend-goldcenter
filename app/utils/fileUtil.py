import os
from typing import List, Optional
import uuid
from anyio import Path
from click import Option
from fastapi import HTTPException, UploadFile
from app.schemas.enums import MediaTypes
from config import ASSETS_URL, CONTENT_TYPES


async def validate_file(file: UploadFile, types: List[MediaTypes], maxSize: float) -> str:

    #checking type of the file uploading
    inValidFormat = True
    for type in types:
        if file.content_type in CONTENT_TYPES[type]: inValidFormat = False
            
    if inValidFormat: raise HTTPException(400, f"Fayl formati noto'g'ri! Sizniki: {file.content_type}")

    file_contents = await file.read()

    filename = f"{uuid.uuid4()}__{file.filename}"

    if len(file_contents) > maxSize * 1024 * 1024:
        raise HTTPException(
            400, f"Fayl kattaligi maksimal {maxSize} MB!")
    
    return filename

async def save_file(file: UploadFile, filename: str, url:Path):

     # set the file offset as 0
    await file.seek(0)
    # read the file contents
    file_contents = await file.read()

    print(len(file_contents))
    
    upload_dir = os.path.join(os.getcwd(), ASSETS_URL, url)
    # Create the upload directory if it doesn't exikst
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

    # get the destination path
    dest = os.path.join(url, filename)

    # save the file
    with open(f"{ASSETS_URL}/{dest}", "wb") as f:
        f.write(file_contents)

async def replace_file(file: Optional[UploadFile] = None, filename: str = ..., replaceWith: str = ..., url:Path = ...):

    if file != None and filename != replaceWith:
        # read the file contents
        file_contents = await file.read()
        
        upload_dir = os.path.join(os.getcwd(), url)
        # Create the upload directory if it doesn't exist
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        # get the destination path
        old_dest = os.path.join(url, filename)
        dest = os.path.join(url, replaceWith)

        # save the file
        with open(f"{ASSETS_URL}/{dest}", "wb") as f:
            f.write(file_contents)

        if os.path.exists(old_dest):
            os.unlink(old_dest)