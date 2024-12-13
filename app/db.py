from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from sqlalchemy.orm import declarative_base

import os 

from dotenv import load_dotenv


class db_connection:
    def __init__(self) -> None:
        self.database_url = '''postgresql://postgres:password@localhost:5432/p2'''
        
        self.create_engine = create_engine(
            self.database_url,
            echo=True
        )
        
        self.session_make = sessionmaker(
            bind=self.create_engine,
            autoflush=False,
            autocommit = False
        )
        
    @contextmanager
    def db_create_session(self):
        session = self.session_make();
        
        try:
            yield session;
        except Exception as e:
            raise e
        finally:
            session.close()
            
db_config = db_connection()
    
Base = declarative_base()