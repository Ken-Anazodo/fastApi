import pytest
from app import models

"""we create a test_vote fixture that creates a new vote in the database for the test user and test post directly without calling the API with a POST request. we use the session fixture to add the new vote to the database and commit the changes. we then return the new vote object so that it can be used in other test functions."""
@pytest.fixture
def test_vote(test_user, test_post, session):
    new_vote = models.Vote(post_id=test_post[3].id, user_id=test_user["id"]) #test_post[3].id is the post id in the test_post fixture with id 4 when also retrieved from the database. 
    session.add(new_vote)
    session.commit()
    print(new_vote)
    return new_vote


def test_vote_on_post(authorized_client, test_post):
    res = authorized_client.post("/vote/", json={"post_id": test_post[3].id, "dir": 1}) #vote on the post test_post[3].id in the test_post fixture with id 4 when also retrieved from the database. 
    assert res.status_code == 201
    assert res.json().get("message") == "Vote added successfully"


def test_vote_twice(authorized_client, test_post, test_vote):
    res = authorized_client.post("/vote/", json={"post_id": test_post[3].id, "dir": 1}) #vote on the post test_post[3].id in the test_post fixture with id 4 when also retrieved from the database. 
    assert res.status_code == 409
    assert res.json().get("detail") == f"User {test_vote.user_id} has already voted on post {test_vote.post_id}"
    
    
def test_delete_vote(authorized_client, test_post, test_vote): #it calls test_vote fixture to create a new vote in the database and we try to remove the vote on the post test_post[3].id to see if the vote is removed successfully. we use the authorized_client fixture to simulate an authenticated request to the /vote/ endpoint with the post_id and dir=0 in the request body. we then assert that the response status code is 201 and the message in the response is "Vote removed successfully".
    res = authorized_client.post("/vote/", json={"post_id": test_post[3].id, "dir": 0}) #remove vote on the post test_post[3].id in the test_post fixture with id 4 when also retrieved from the database. 
    assert res.status_code == 201
    assert res.json().get("message") == "Vote removed successfully"
    
    
def test_delete_vote_not_exist(authorized_client, test_post): #we try to remove a vote on the post test_post[3].id that doesn't exist in the database to see if the correct error is raised. we use the authorized_client fixture to simulate an authenticated request to the /vote/ endpoint with the post_id and dir=0 in the request body. we then assert that the response status code is 404 and the detail message in the response is "vote does not exist".
    res = authorized_client.post("/vote/", json={"post_id": test_post[3].id, "dir": 0}) #remove vote on the post test_post[3].id in the test_post fixture with id 4 when also retrieved from the database. 
    assert res.status_code == 404
    assert res.json().get("detail") == "vote does not exist"
    
    
def test_vote_on_post_not_exist(authorized_client): #we try to vote on a post with id 999 that doesn't exist in the database to see if the correct error is raised. we use the authorized_client fixture to simulate an authenticated request to the /vote/ endpoint with the post_id and dir=1 in the request body. we then assert that the response status code is 404 and the detail message in the response is "post with id: 999 does not exist".
    res = authorized_client.post("/vote/", json={"post_id": 999, "dir": 1}) #vote on the post with id 999 that doesn't exist in the database. 
    assert res.status_code == 404
    assert res.json().get("detail") == "post with id: 999 does not exist"
    
    
def test_vote_unauthorized_user(client, test_post): #we try to vote on a post with id 4 without being authenticated to see if the correct error is raised. we use the client fixture to simulate an unauthenticated request to the /vote/ endpoint with the post_id and dir=1 in the request body. we then assert that the response status code is 401 and the detail message in the response is "Not authenticated".
    res = client.post("/vote/", json={"post_id": test_post[3].id, "dir": 1}) #vote on the post test_post[3].id in the test_post fixture with id 4 when also retrieved from the database. 
    assert res.status_code == 401
    assert res.json().get("detail") == "Not authenticated" #Not authenticated is the default error message returned by FastAPI when a user is not authenticated and tries to access a protected endpoint.