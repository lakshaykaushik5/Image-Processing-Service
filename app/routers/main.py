from fastapi import FastAPI,HTTPException,Response,Request, Cookie,File,UploadFile,APIRouter,Depends
from fastapi.security import HTTPBearer
from middleware.auth_middleware import authenticate_middleware
from type_schema import Upload_Image
from services.main_service import upload_image
import os

main_router = APIRouter(prefix="/main",tags=["main"])

UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@main_router.get("/")
async def main():
    return {"msg":"working main service"}

@main_router.post("/upload_file")
async def upload_file(req:Upload_Image,res:Response):
    return upload_image(req,res)