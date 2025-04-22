from fastapi import APIRouter, UploadFile, File

from src.services.users.controller import ChatBuilder
from src.services.users.serializer import QuestionInput
router = APIRouter(prefix="/v1/ai")


@router.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    return await ChatBuilder().upload_csv_to_s3(file)

@router.post("/csv-open-ai")
# @router.post("/conversation/{conversationId}")
async def open_ai_csv_question(request:QuestionInput):
    return await ChatBuilder().open_ai_csv_question(
        request = request
    )