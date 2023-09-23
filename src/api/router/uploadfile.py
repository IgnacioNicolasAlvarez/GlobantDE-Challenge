from fastapi import APIRouter, HTTPException, UploadFile

router = APIRouter(
    prefix="/uploadfile",
    tags=["uploadfile"],
    responses={404: {"description": "Not found"}},
)


@router.post("/upload/")
async def upload(file: UploadFile):
    if not file.filename.endswith(".csv"):
        raise HTTPException(
            status_code=406, detail="The only allowed file extension is .csv"
        )

    try:
        contents = await file.read()
    except Exception as _:
        raise HTTPException(status_code=500, detail="Error trying to read the file")

    return {"filename": file.filename, "content_length": len(contents)}
