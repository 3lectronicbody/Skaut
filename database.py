from sqlalchemy.orm import sessionmaker
from models import Base
from sqlalchemy import create_engine
import json




class Database:
    def __init__(self):
        with open("config.json") as f:
            data = json.load(f)
            database_url = data["database_url"]
        self.engine = create_engine(database_url, echo=False)
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def session(self):
        return self.SessionLocal()
