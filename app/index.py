from fastapi import FastAPI, APIRouter
from routers.authenticaion_router import auth_router
from routers.main import main_router
import uvicorn

app = FastAPI()

app.include_router(auth_router)
app.include_router(main_router)


# @app.middleware('http')
@app.get("/")
async def root():
    return {"msg":"API"}


# ---------------------------------------------------------------------
if __name__ == "__main__":                                          
    uvicorn.run(app,host="localhost",port=4444)                     
# ---------------------------------------------------------------------