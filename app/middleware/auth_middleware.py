from fastapi import FastAPI,HTTPException,Response,Request, Cookie,File,UploadFile,APIRouter
from fastapi.security import HTTPBearer
from type_schema import SignUp,LogIn
import jwt
import os

# -----------to be put on env ------------------

jwt_secret = os.getenv("JWT_SECRET") or "secret_key"
algo = os.getenv("ALGORITHM") or "HS256"
jwt_refresh_secret = "refresh_secret_key"


# ----------------------------------------------

async def authenticate_middleware(req:Request):
    
    try:
        print("hello world")
        
        access_token = req.cookies.get("access_token")
        if not access_token:
            raise HTTPException(status_code=404,detail="Token Required")
        
        decode_data = jwt.decode(access_token,jwt_secret,algo)
        
        req.user = decode_data
        
    except Exception as err:
        
        if err.name == "TokenExpiredError":
            raise HTTPException(status_code=401,detail="Token Expired")
        
        raise HTTPException(status_code=500,detail=f"An error occured ::: {err}")
    
    # res = await call_next(req)
    # return res