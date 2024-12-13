from fastapi import FastAPI,HTTPException,Response,Request, Cookie
from fastapi.security import HTTPBearer
import uvicorn
from type_schema import SignUp,LogIn,Payload
import jwt
import os
from db import db_config
from models import master_users
import bcrypt
import binascii


jwt_secret = os.getenv("JWT_SECRET") or "secret_key"
algo = os.getenv("ALGORITHM") or "HS256"
jwt_refresh_secret = "refresh_secret_key"

app = FastAPI()



@app.get("/")
def server():
    print("server started ...............")
    return

def generate_access_token(payload:Payload):
    token = jwt.encode(payload,
                       jwt_secret,
                       algo)
    
    return token

def generate_refresh_token(payload:Payload):
    token = jwt.encode(payload,jwt_refresh_secret,algo)
    return token

async def authenticate_middleware(req:Request,call_next):
    
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
    
    res = await call_next(Request)
    return res

def signUp_service(req_data:SignUp,response:Response):
    try:
        user_email = req_data.useremail
        user_password = req_data.password
        user_name = user_email.split("@")[0]
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(user_password.encode("utf-8"),salt)
        
        
        
        with db_config.db_create_session() as session:
            
            existing_user = session.query(master_users).filter_by(useremail = user_email).first()
            if existing_user:
                raise HTTPException(status_code=400,detail="user already exists")
            
            add_user = master_users(useremail=user_email,username = user_name,password = hashed_password)
            
            
            
            session.add(add_user)
            session.commit()
            new_user = session.query(master_users).filter_by(useremail=user_email).first()
            
            
            
            payload = {"user_id":new_user.master_id,
                       "useremail":user_email,
                       "username":user_name,
                       "role":new_user.role,
                       "refresh_token_version":new_user.refresh_token_version}
        
            payload_refresh = {
                "user_id":new_user.master_id,
                "refresh_token_version":new_user.refresh_token_version
            }
            
            access_token = generate_access_token(payload)
            refresh_token = generate_refresh_token(payload_refresh)
            
            
            
            # --------------update-user-------------------------

            session.query(master_users).filter_by(useremail=user_email).update({
                "refresh_token":refresh_token
            })
            session.commit()
        
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=15*60*1000
        )
        
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=7*24*60*60*1000
        )
        
        response.status_code = 200
        return {"access_token":access_token,"refresh_token":refresh_token}
        
                
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"An error occurred: {err}")


def logIn_service(req_data:LogIn,res:Response):
    try:
        user_email = req_data.useremail
        user_password = req_data.password
         
        with db_config.db_create_session() as session:
            check = session.query(master_users).filter_by(useremail=user_email).first()
            
            if not check or check == None:
                raise HTTPException(status_code=404,detail=f"User Not Found")
            
            
            
            stored_password = None
            
            hex_password=check.password
            
            if hex_password.startswith('\\x'):
                hex_password = hex_password[2:]
                
                stored_password = binascii.unhexlify(hex_password)


            
            val_check = bcrypt.checkpw(user_password.encode("utf-8"),stored_password)
            
            
            if not val_check:
                raise HTTPException(status_code=401,detail="Invalid Password")
            
            access_payload = {"user_id":check.master_id,
                              "useremail":check.useremail,
                              "username":check.username,
                              "role":check.role,
                              "refresh_token_version":check.refresh_token_version}
            
            refresh_payload = {"user_id":check.master_id,
                               "refresh_token_version":check.refresh_token_version}
            
            access_token = generate_access_token(access_payload)
            refresh_token = generate_refresh_token(refresh_payload)
            
            session.query(master_users).filter_by(useremail=user_email).update({"refresh_token":refresh_token})
            
            session.commit()
            
        res.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=15*60*1000
        )
        
        res.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=7*24*60*60*1000
        )
        
        res.status_code = 200
        return {"access_token":access_token,"refresh_token":refresh_token}
            
            
    except Exception as err:
        raise HTTPException(status_code=500,detail=f"An error occured: {err}")


def refresh_service(req:Request,res:Response):
    try:
        token = req.cookies.get("refresh_token")
        if not token:
            raise HTTPException(status_code=404,detail="Token required")
        
        decode_data = jwt.decode(token,jwt_refresh_secret,algo)
        
        user_id = decode_data.user_id
        refresh_token_version = decode_data.refresh_token_version
        
        with db_config.db_create_session() as session:
            user_data = session.query(master_users).filter_by(master_id = user_id).first()
            
            if user_data.refresh_token_version != refresh_token_version:
                raise HTTPException(status_code=401,detail="refresh token expired")
            
            access_payload = {"user_id":user_id,
                              "useremail":user_data.useremail,
                              "username":user_data.username,
                              "role":user_data.role,
                              "refresh_token_version":refresh_token_version+1
                              }
            
            refresh_payload = {
                "user_id":user_id,
                "refresh_token_version":refresh_token_version+1
            }
            
            access_token = generate_access_token(access_payload)
            refresh_token = generate_refresh_token(refresh_payload)
            
            session.query(master_users).filter_by(master_id = user_id).update({"refresh_token":refresh_token,"refresh_token_version":refresh_token_version+1})
            
            session.commit()
        res.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=15*60*1000
        )
        
        res.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=7*24*60*60*1000
        )
        
        res.status_code = 200
        return {"token":token,"refresh_token":refresh_token}
        
    except Exception as err:
        raise HTTPException(status_code=500,detail=f"An error occoured {err}")


def logout_service(req:Request,res:Response):
    try:
        res.delete_cookie("access_token")
        res.delete_cookie("refresh_token")
    except Exception as err:
        raise HTTPException(status_code=500,detail=f"An error occured ::: {err}")


@app.post("/sign_up")
def signUp(req_data:SignUp,res:Response):
    
    return signUp_service(req_data,res)
    
@app.post("/log_in")
def logIn(req_data:LogIn,res:Response):
    
    return logIn_service(req_data,res)

@app.get("/refresh")
def refresh(req:Request,res:Response):
    
    return refresh_service(req,res)
    
@app.middleware(authenticate_middleware)
@app.post("/logout")
def logout(req:Request,res:Response):
    
    return logout_service(req,res)
    

# ---------------------------------------------------------------------
if __name__ == "__main__":                                          
    uvicorn.run(app,host="localhost",port=4444)                     
# ---------------------------------------------------------------------