from fastapi import APIRouter, UploadFile, status, HTTPException
import os
import uuid

file_router = APIRouter()


@file_router.post("/file/upload")
async def upload_xml(file : UploadFile):

    file_extention = file.filename.split(".")[-1]
    
    if file_extention != "xml":
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="file format not supported"
        )
    
    unique_id = str(uuid.uuid4())
    save_path = os.path.join("input_file", unique_id)
    os.makedirs(save_path, exist_ok=True)

    file_path = os.path.join(save_path, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())


    return{
        "status" : status.HTTP_200_OK,
        "message" : "file Uploaded successfully",
        "filepath" : f"input_file/{unique_id}/{file.filename}"
    }


@file_router.delete("file/{file_path:path}")
def delete_file(file_path : str):
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail=f"File not found: {file_path}"
        )
    
    try:
        os.remove(file_path)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while deleting the file: {str(e)}"
        )
    
    return {
        "status" : status.HTTP_200_OK,
        "message" : 'file deleted successfully',
        "file_path" : file_path
    }