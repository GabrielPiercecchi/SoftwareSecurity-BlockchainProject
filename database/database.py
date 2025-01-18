from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

class DBIsConnected:
    _instance = None

    def __init__(self):
        if DBIsConnected._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            DBIsConnected._instance = self
            self.engine = create_engine(
                f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:{os.getenv('DATABASE_PORT_FASK_APP')}/{os.getenv('DATABASE_NAME')}"
            )
            self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            
    @staticmethod
    def get_instance():
        if DBIsConnected._instance is None:
            DBIsConnected()
        return DBIsConnected._instance

    def get_session(self):
        return self.SessionLocal()

# Usage example:
# db_instance = DBIsConnected.get_instance()
# session = db_instance.get_session()