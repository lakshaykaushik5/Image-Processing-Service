from pydantic import BaseModel
from fastapi import FastAPI,HTTPException,Response,Request, Cookie,File,UploadFile,APIRouter,Depends


class SignUp(BaseModel):
    useremail:str
    password:str
    
class LogIn(BaseModel):
    useremail:str
    password:str
    
class Payload(BaseModel):
    user_id:int
    useremail:str
    username:str
    role:int
    refresh_token_version:int
    
class Refresh_Payload(BaseModel):
    user_id:int
    refresh_token_version:int
    
class Upload_Image(BaseModel):
    user_id:int
    image_name:str
    img_file:UploadFile=File(...)