# import pytest
# from fastapi.testclient import TestClient
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from app.database import get_db, Base
# from app.main import app
# from app.config import settings
# from alembic import command #this is used to run the alembic commands in the test file. 



# # SQL_ALCHEMY_DATABASE_URL = "postgresql://postgres:password123@localhost:5432/fastapi_test" we can use this or the alternative below to connect to the fastapi_test database created.
# SQL_ALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}_test" #This is your connection string

# engine = create_engine(SQL_ALCHEMY_DATABASE_URL) #engine is what's responsible for allowing sqlalchemy to connect to a postgres database. it is responsible for establishing the connection to a database.

# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #This is what we use to actually create a database session. we make use of a session when we want to talk to a sql database.





# """USING ALEMBIC TO MIGRATE THE DATABASE DURING TESTING"""
# # def client():
# #     command.upgrade("head")
# #     command.downgrade("base")
# #     yield TestClient(app)



# """USING SQLALCHEMY ORM TO INTERACT WITH THE DATABASE (We made use of this approach because it's a quicker way to run and setup our tests)"""

# """A Fixture that returns a database object to manipulate data directly in the database."""
# @pytest.fixture
# def session():
#     Base.metadata.drop_all(bind=engine) #drop the tables in the database before we run our tests. This is to ensure that we have a clean slate before we run our tests. It also cleans up the database and prevent memory leaks. Using drop_all above like we did is beneficial because it helps in debugging  when we want to see the current state of our database when it failed when running our tests
#     Base.metadata.create_all(bind=engine)#create the tables in the database before we run our tests. 
#     db = TestingSessionLocal() # is used to talk to the database. It is used to create a new session with the database and return it to the path operation. The session is used to interact with the database and perform CRUD operations.
#     try: 
#         yield db # This is used to return the database session to the path operation. It is used to create a new session with the database and return it to the path operation. The session is used to interact with the database and perform CRUD operations.
#     finally: # This is used to ensure that the database session is closed after the request is completed. It is used to clean up resources and prevent memory leaks.
#         db.close()


# """A Fixture that returns a TestClient object to simulate requests to the API and test the endpoints."""
# @pytest.fixture
# def client(session):
#     #run our code before we run our test
#     """This is a dependency that will be used to create a database session. It will be used in the path operations(endpoints) to get a database session for every request and use it to interact with the database."""
#     def override_get_db():
#         try: 
#             yield session 
#         finally: 
#             session.close()
    
#     app.dependency_overrides[get_db] = override_get_db #This is used to override the get_db dependency with the override_get_db function. It is used to create a new session with the database and return it to the path operation. You can find this if you search for dependencies in fastapi documentation
#     yield TestClient(app) #yield is used to return the TestClient instance to the test function. It is used to create a new instance of the TestClient and return it to the test function. The TestClient is used to simulate requests to the API and test the endpoints.
#     #run our code after we run our test
#     #<---- code (if any)---->



