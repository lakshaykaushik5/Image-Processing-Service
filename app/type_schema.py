from pydantic import BaseModel

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