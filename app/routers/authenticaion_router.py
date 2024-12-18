from fastapi import FastAPI,HTTPException,Response,Request, Cookie,File,UploadFile,APIRouter,Depends
from fastapi.security import HTTPBearer
from type_schema import SignUp,LogIn
from middleware.auth_middleware import authenticate_middleware
# from services.auth_service import signUp_service,logIn_service,refresh_service,logout_service

from services.auth_service import signUp_service,logIn_service,refresh_service,logout_service


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/sign_up")
def signUp(req_data:SignUp,res:Response):
    
    print("----------GOT-HERE--------------")
    
    return signUp_service(req_data,res)
    
@auth_router.post("/log_in")
def logIn(req_data:LogIn,res:Response):
    
    return logIn_service(req_data,res)

@auth_router.get("/refresh")
def refresh(req:Request,res:Response):
    
    return refresh_service(req,res)
    
@auth_router.post("/logout")
def logout(req:Request,res:Response):
    
    return logout_service(req,res)