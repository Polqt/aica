from .base_class import Base
from .session import engine
from . import models

def init_db():
    print('Creating database tables...')
    Base.metadata.create_all(bind=engine)
    print('Database tables created successfully.')