"""conftest is a package specific and package scoped so fixtures are auto detected by pytest 
in some test modules and not in others i.e children packages of the tests folder with their 
own conftest.py files is only scoped to their individual packages respectively while 
the root conftest.py file in the tests folder is scoped to the entire tests folder. 
It is a special configuration file for pytest that 
allows us to define fixtures and other configurations that can be shared 
across multiple test files. It is automatically detected by pytest and does not need 
to be imported in the test files. This is useful for setting up common test data, 
setting up mock objects, creating  ```database connections, or any other setup that needs 
to be done before running the tests. In this case, we are using conftest.py to define fixtures 
for the database session, test client, and a test user that can be used in our test files."""


import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base
from app.main import app
from app.config import settings
from alembic import command #this is used to run the alembic commands in the test file. 
from app import models
from app.oauth2 import create_access_token



# SQL_ALCHEMY_DATABASE_URL = "postgresql://postgres:password123@localhost:5432/fastapi_test" we can use this or the alternative below to connect to the fastapi_test database created.
SQL_ALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}_test" #This is your connection string

engine = create_engine(SQL_ALCHEMY_DATABASE_URL) #engine is what's responsible for allowing sqlalchemy to connect to a postgres database. it is responsible for establishing the connection to a database.

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #This is what we use to actually create a database session. we make use of a session when we want to talk to a sql database.



"""USING ALEMBIC TO MIGRATE THE DATABASE DURING TESTING"""
# def client():
#     command.upgrade("head")
#     command.downgrade("base")
#     yield TestClient(app)



"""USING SQLALCHEMY ORM TO INTERACT WITH THE DATABASE (We made use of this approach because it's a quicker way to run and setup our tests)"""

"""The type of fixtures we're using are function scoped fixtures because they are created and destroyed for each test function that uses them.
This is useful for ensuring that each test function has a clean slate to work with and that any changes made to the database during a test function do not affect other test functions. 
This is important because we want to ensure that our tests are isolated and do not interfere with each other. 
"""

"""A Fixture that returns a database object to manipulate data directly in the database."""
@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine) #drop the tables in the database before we run our tests. This is to ensure that we have a clean slate before we run our tests. It also cleans up the database and prevent memory leaks. Using drop_all above like we did is beneficial because it helps in debugging  when we want to see the current state of our database when it failed when running our tests
    Base.metadata.create_all(bind=engine)#create the tables in the database before we run our tests. 
    db = TestingSessionLocal() # is used to talk to the database. It is used to create a new session with the database and return it to the path operation. The session is used to interact with the database and perform CRUD operations.
    try: 
        yield db # This is used to return the database session to the path operation. It is used to create a new session with the database and return it to the path operation. The session is used to interact with the database and perform CRUD operations.
    finally: # This is used to ensure that the database session is closed after the request is completed. It is used to clean up resources and prevent memory leaks.
        db.close()


"""A Fixture that returns a TestClient object to simulate requests to the API and test the endpoints. It uses the session fixture to create a new session with the database and return it to the path operation."""
@pytest.fixture
def client(session):
    #run our code before we run our test
    """This is a dependency that will be used to create a database session. It will be used in the path operations(endpoints) to get a database session for every request and use it to interact with the database."""
    def override_get_db():
        try: 
            yield session 
        finally: 
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db #This is used to override the get_db dependency with the override_get_db function. It is used to create a new session with the database and return it to the path operation. You can find this if you search for dependencies in fastapi documentation
    yield TestClient(app) #yield is used to return the TestClient instance to the test function. It is used to create a new instance of the TestClient and return it to the test function. The TestClient is used to simulate requests to the API and test the endpoints.
    #run our code after we run our test
    #<---- code (if any)---->
    
"""This creates and returns a new user. it uses the client fixture to simulate a post request to the /users/ endpoint with the email and password of the new user. it then asserts that the response status code is 201 and returns the new user as a dictionary. this fixture can be used in other test functions to create a new user and test the endpoints that require authentication."""    
@pytest.fixture
def test_user(client):
    user_data = {"email": "test@gmail.com", "password": "password123"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    # print(response.json())
    new_user["password"] = user_data["password"]
    # print(new_user)
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "test123@gmail.com", "password": "password123"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    # print(response.json())
    new_user["password"] = user_data["password"]
    # print(new_user)
    return new_user

"""This fixture ensures when a that the test user is authenticated before making requests to the API. it uses the token fixture to create a new access token for the test user and adds it to the headers of the TestClient instance. this allows us to simulate authenticated requests to the API and test the endpoints that require authentication."""
@pytest.fixture
def token(test_user):
    return create_access_token(data={"user_id": test_user["id"]})

"""This fixture ensures when a that the test user is authenticated before making requests to the API. it uses the token fixture to create a new access token for the test user and adds it to the headers of the TestClient instance. this allows us to simulate authenticated requests to the API and test the endpoints that require authentication."""
@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client



"""Testing the create post endpoint to ensure that the post is created successfully and the response is as expected. we use the authorized_client fixture to simulate a post request to the /posts/ endpoint with the title and content of the new post. we then assert that the response status code is 201 and the title of the new post in the response matches the title we sent in the request. we also assert that the owner_id of the new post in the response matches the id of the test_user created in the test_user fixture. we use the schemas.Post model to validate the response data and ensure that it matches the expected schema for a post object."""
@pytest.fixture
def test_post(test_user, session, test_user2):
    post_data = [
        {
            "title": "Test Post",
            "content": "This is a test post.",
            "owner_id": test_user["id"]
        },
        {
            "title": "Test Post 2",
            "content": "This is a test post 2.",
            "owner_id": test_user["id"]
        },
        {
            "title": "Test Post 3",
            "content": "This is a test post 3.",
            "owner_id": test_user["id"]
        },
        {
            "title": "Test Post 4",
            "content": "This is a test post 4.",
            "owner_id": test_user2["id"]
        }
    ]
    
    """1st alternative way to add posts to the database using map() function and unpacking the dictionary returned by the post_data list and passing it as keyword arguments to the Post model constructor. so even if we add more fields(column) to the post_data list, we don't have to change the code here, it will automatically unpack the dictionary and pass it as keyword arguments to the Post model constructor. it is the same as writing new_post = models.Post(title=post["title"], content=post["content"], owner_id=post["owner_id"]) but it is more flexible and scalable. it is a better way to create a new instance of the Post model with the data received in the request body."""
    def create_post_model(post):
        return models.Post(**post) #this creates a new instance of the Post model with data received in the request body or in our case each of the dictionary from the post_data list. it uses the ** operator to unpack the dictionary returned by the post_data list and pass it as keyword arguments to the Post model constructor. so even if we add more fields(column) to the post_data list, we don't have to change the code here, it will automatically unpack the dictionary and pass it as keyword arguments to the Post model constructor. it is the same as writing new_post = models.Post(title=post["title"], content=post["content"], owner_id=post["owner_id"]) but it is more flexible and scalable. it is a better way to create a new instance of the Post model with the data received in the request body or in our case the dictionary from the post_data list.

    post_map = map(create_post_model, post_data) #This creates a map object that contains the Post model instances created from each of the dictionary in the post_data list and it returns a map. it is a better way to create a new instance of the Post model with the dictionary received from the post_data list.
    posts = list(post_map) #this converts the map object to a list of Post model instances that can be added to the database session.
    session.add_all(posts)
    
    
    """2nd alternative way to add posts to the database using session.add_all() method"""
    # session.add_all([
    #     models.Post(title="Test Post", content="This is a test post.", owner_id=test_user["id"]),
    #     models.Post(title="Test Post 2", content="This is a test post 2.", owner_id=test_user["id"]),
    #     models.Post(title="Test Post 3", content="This is a test post 3.", owner_id=test_user["id"]),
    #     models.Post(title="Test Post 4", content="This is a test post 4.", owner_id=test_user2["id"])
    #     ])
    
    session.commit()
    
    posts = session.query(models.Post).all()
    return posts

   
    
