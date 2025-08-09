from .base_class import Base
from .session import engine
from . import models

def init_db():
    print("Dropping existing tables...")
    Base.metadata.drop_all(bind=engine)  
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)  
    print("Database reset and tables created successfully.")