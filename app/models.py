from sqlalchemy import Column,Integer,String,DateTime,Boolean

import datetime
from db import Base,db_config


class master_users(Base):
    __tablename__ = "master_users"
    
    master_id = Column(Integer,primary_key=True,index=True)
    username = Column(String,default=None)
    useremail = Column(String,unique=True,nullable=False)
    password = Column(String,default=None)
    refresh_token = Column(String,default=None)
    refresh_token_version = Column(Integer,default=0)
    role = Column(Integer,default=0)
    status = Column(Boolean,default=True)
    created_at = Column(DateTime,default=datetime.datetime.utcnow)
    updated_at = Column(DateTime,default=datetime.datetime.utcnow,onupdate=datetime.datetime.utcnow)
    

class master_images(Base):
    __tablename__ = "master_images"
    
    image_id = Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer,default=None)
    image_name = Column(String,default=None)
    created_at = Column(DateTime,default=datetime.datetime.utcnow)
    updated_at = Column(DateTime,default=datetime.datetime.utcnow,onupdate=datetime.datetime.utcnow)
    

Base.metadata.create_all(bind=db_config.create_engine)
    
        