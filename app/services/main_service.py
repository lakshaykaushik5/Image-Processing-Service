from fastapi import FastAPI,HTTPException,Response,Request, Cookie,File,UploadFile,APIRouter,Depends,Form
from fastapi.security import HTTPBearer
from db import db_config
from type_schema import Upload_Image
from models import master_images
import os
import shutil

# -----------to-be-put-on-env----------
UPLOAD_DIR = "uploaded_images"
# -------------------------------------

# async def upload_image(req:Upload_Image,res:Response):
    
#     u_id = req.user_id
#     img_name = req.image_name
#     img_file = req.img_file
#     if not img_file.filename.endswith((".png",".jpg",".jpeg",".gif")):
#         raise HTTPException("Un Supported File")
    
#     file_location = os.path.join(UPLOAD_DIR,img_file.filename)
    
#     with open(file_location,'wb') as buffer:
#         shutil.copyfileobj(img_file.file,buffer)
        
#     with db_config.db_create_session() as session:
#         add_image = master_images(user_id=u_id,image_name=img_name)
#         session.add(add_image)
#         session.commit()
        
#     return {"filename":img_name,"message":"Image uploaded successfully"}

async def upload_image(
    user_id: int = Form(...), 
    image_name: str = Form(...), 
    img_file: UploadFile = File(...)
):
    # Validate file extension
    if not img_file.filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
        raise HTTPException(status_code=415, detail="Unsupported File Type")

    # Ensure upload directory exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Generate a unique file name to avoid overwriting
    file_location = os.path.join(UPLOAD_DIR, f"{user_id}_{image_name}")

    try:
        # Save the file
        with open(file_location, "wb") as buffer:
            content = await img_file.read()
            buffer.write(content)

        # Save metadata to database
        with db_config.db_create_session() as session:
            add_image = master_images(user_id=user_id, image_name=image_name)
            session.add(add_image)
            session.commit()

        return {"filename": image_name, "message": "Image uploaded successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
