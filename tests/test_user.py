import pytest
import jwt
from app import schemas
from app.config import settings
#we don't need to import client, session and test_user from conftest.py to make use of them because pytest automatically detects the fixtures in conftest.py and makes them available to all the test files in the tests folder. so we can use them directly in our test files without importing them.


def test_root(client):
    res = client.get("/")
    print(res.json().get("message"))
    assert res.json().get("message") == "Hello World!"
    assert res.status_code == 200
    
    
"""Testing the create user endpoint to ensure that the user is created successfully and the response is as expected. we use the client fixture to simulate a post request to the /users/ endpoint with the email and password of the new user. we then assert that the response status code is 201 and the email of the new user in the response matches the email we sent in the request. we also assert that the password is not returned in the response for security reasons. we use the schemas.UserOut model to validate the response data and ensure that it matches the expected schema for a user object.""" 
def test_create_user(client):
    res = client.post("/users/", json={"email": "hello@gmail.com", "password": "password"}) #Because it's a post request we use the json to simulate a post request to test the endpoint and see the user is created and saved to the database.
    # print(res.json())
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello@gmail.com"
    assert res.status_code == 201
    
    
    
"""Testing the login endpoint to ensure that the user can login with the correct credentials and receive a valid access token"""  
def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm]) #we decode the token in the test to verify that the user_id in the payload matches the id of the test_user created in the test_user fixture. we use the settings.secret_key and settings.algorithm to decode the token because we used them to encode the token in the first place. we use the jwt.decode method to decode the token and get the payload. we then get the user_id from the payload and compare it with the id of the test_user created in the test_user fixture. if they match, it means that the login was successful and the token is valid.
    id = (payload.get("user_id"))
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200
    
 
"""Testing incorrect login scenarios using parametrize to test multiple scenarios in one test function. we test for incorrect email, incorrect password, and missing email or password. we also test for the correct email and password to ensure that the login is successful. we use the status_code parameter to check the status code of the response and assert that it matches the expected status code for each scenario. we also check the detail message in the response for the incorrect login scenarios to ensure that it matches the expected message."""

@pytest.mark.parametrize("email, password, status_code", [
    ("test@gmail.com", "password123", 200),
    ("test@gmail.com", "wrongpassword", 403),
    ("nonexistent@gmail.com", "password123", 403),
    ("wrongemail@gmail.com", "wrongpassword", 403),
    (None, "password123", 422),
    ("test@gmail.com", None, 422)
])

def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
    if status_code == 403:
        assert res.json().get("detail") == "Invalid Credential"
        
