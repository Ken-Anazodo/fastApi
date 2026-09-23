from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


"""UNIQUE URL TO CONNECT TO THE DATABASE"""
# SQL_ALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address/localhost>/<database_name>"
# SQL_ALCHEMY_DATABASE_URL = "postgresql://postgres:12345@localhost:5432/fastapi" #This is your connection string
SQL_ALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}" #This is your connection string

engine = create_engine(SQL_ALCHEMY_DATABASE_URL) #engine is what's responsible for allowing sqlalchemy to connect to a postgres database. it is responsible for establishing the connection to a database.

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #This is what we use to actually create a database session. we make use of a session when we want to talk to a sql database.

Base = declarative_base() #This is the base class that we'll use to create our models.The models are going to be extending the base class.


"""This is a dependency that will be used to create a database session. It will be used in the path operations(endpoints) to get a database session for every request and use it to interact with the database."""
def get_db():
    db = SessionLocal() # is used to talk to the database. It is used to create a new session with the database and return it to the path operation. The session is used to interact with the database and perform CRUD operations.
    try: 
        yield db # This is used to return the database session to the path operation. It is used to create a new session with the database and return it to the path operation. The session is used to interact with the database and perform CRUD operations.
    finally: # This is used to ensure that the database session is closed after the request is completed. It is used to clean up resources and prevent memory leaks.
        db.close()  