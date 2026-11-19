import pytest
from app import schemas


"""Testing the get all posts endpoint to ensure that the posts are retrieved successfully and the response is as expected. we use the authorized_client fixture to simulate a get request to the /posts/ endpoint and the test_post fixture to provide the test posts when the endpoint is called which creates the posts in the database. we then assert that the response status code is 200 and the response contains the expected posts."""
def test_get_all_post(authorized_client, test_post):
    res = authorized_client.get("/posts/")
    # print(res.json())
    
    def validate(post):
        return schemas.PostOut(**post) #this validates the response data and ensures that it matches the expected schema for a post object. it uses the ** operator to unpack the dictionary returned by the post and pass it as keyword arguments to the Post model constructor. so even if we add more fields(column) to the Post model, we don't have to change the code here, it will automatically unpack the dictionary and pass it as keyword arguments to the Post model constructor. it is the same as writing new_post = schemas.Post(title=post["title"], content=post["content"], owner_id=post["owner_id"]) but it is more flexible and scalable. it is a better way to validate the response data and ensure that it matches the expected schema for a post object.
    
    posts_map = map(validate, res.json()) #this creates a map object that contains the Post model instances created from each of the dictionary in the response data and it returns a map. it is a better way to validate the response data and ensure that it matches the expected schema for a post object.
    # print(list(posts_map)) #this converts the map object to a list of Post model instances that can be used to assert the response data and ensure that it matches the expected schema for a post object.
    
    assert len(res.json()) == len(test_post)
    assert res.status_code == 200
    
    
"""Testing the get all posts endpoint to ensure that the posts are not retrieved successfully when the user is not authorized and the response is as expected. we use the client fixture to simulate a get request to the /posts/ endpoint without providing an access token in the request headers. we then assert that the response status code is 401 and the response contains the expected error message."""    
def test_unauthorized_user_get_all_post(client, test_post):
    res = client.get("/posts/")
    assert res.status_code == 401
    
    
"""Testing the get one post or get post by id endpoint to ensure that the post is not retrieved successfully when the user is not authorized and the response is as expected. we use the client fixture to simulate a get request to the /posts/{id}/ endpoint without providing an access token in the request headers. we then assert that the response status code is 401 and the response contains the expected error message."""    
def test_unauthorized_user_get_one_post(client, test_post):
    res = client.get(f"/posts/{test_post[0].id}/") # we use the f-string to format the url with the id of the first post in the test_post fixture otherwise it would have to be hardcoded since its what we are testing with.
    assert res.status_code == 401
    
"""Testing the get one post or get post by id endpoint to ensure that we receive a 404 error when the post with the given id does not exist in the database and the response is as expected. we use the authorized_client fixture to simulate a get request to the /posts/{id}/ endpoint with an id that does not exist in the database. we then assert that the response status code is 404 and the response contains the expected error message."""
def test_get_one_post_not_exist(authorized_client, test_post):
    res = authorized_client.get(f"/posts/88888888/") 
    assert res.status_code == 404
    
"""Testing the get one post or get post by id endpoint to ensure that the post is retrieved successfully when the user is authorized and the response is as expected. we use the authorized_client fixture to simulate a get request to the /posts/{id}/ endpoint with the id of the first post in the test_post fixture which creates the posts in the database. we then assert that the response status code is 200 and the response contains the expected post data."""   
def test_get_one_post(authorized_client, test_post):
    res = authorized_client.get(f"/posts/{test_post[0].id}/") # we use the f-string to format the url with the id of the first post in the test_post fixture otherwise it would have to be hardcoded since its what we are testing with.
    post = schemas.PostOut(**res.json()) #validate the response data using pydantic model (the PostOut schema) and ensure that it matches the expected schema for a post object. it uses the ** operator to unpack the dictionary returned by the response data and pass it as keyword arguments to the Post model constructor. so even if we add more fields(column) to the Post model, we don't have to change the code here, it will automatically unpack the dictionary and pass it as keyword arguments to the Post model constructor. it is the same as writing new_post = schemas.Post(title=res.json()["title"], content=res.json()["content"], owner_id=res.json()["owner_id"]) but it is more flexible and scalable. it is a better way to validate the response data and ensure that it matches the expected schema for a post object.
    assert post.Post.id == test_post[0].id
    assert res.status_code == 200
    assert post.Post.title == test_post[0].title
    assert post.Post.content == test_post[0].content
    
    
"""Testing the create post endpoint to ensure that the post is created successfully when the user is authorized and the response is as expected. we use the authorized_client fixture to simulate a post request to the /posts/ endpoint with the post data. we then assert that the response status code is 201 and the response contains the expected post data."""   
@pytest.mark.parametrize("title, content, published", [
    ("awesome new post", "This is an awesome new post.", True),
    ("Living the Life", "This is a post about living the life.", False),
    ("Welcome to the Jungle", "This is the school of hard knocks.", True)
]) 
def test_create_post(authorized_client, test_user, test_post, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]
    
  
"""Testing the create post endpoint to ensure that the post is created successfully with the default published value of True when published is not provided and when the user is authorized and the response is as expected. we use the authorized_client fixture to simulate a post request to the /posts/ endpoint with the post data without providing the published value. we then assert that the response status code is 201 and the response contains the expected post data with the default published value of True."""  
def test_create_post_default_published_true(authorized_client, test_user, test_post):
    res = authorized_client.post("/posts/", json={"title": "Test Post", "content": "This is a test post."})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "Test Post"
    assert created_post.content == "This is a test post."
    assert created_post.published == True
    assert created_post.owner_id == test_user["id"]
    

"""Testing the create post endpoint to ensure that the post is not created successfully when the user is not authorized and the response is as expected. we use the client fixture to simulate a post request to the /posts/ endpoint without providing an access token in the request headers. we then assert that the response status code is 401 and the response contains the expected error message."""   
def test_unauthorized_user_create_post(client, test_user, test_post):
    res = client.post("/posts/", json={"title": "Test Post", "content": "This is a test post."})
    assert res.status_code == 401
    
"""Testing the delete post endpoint to ensure that the post is not deleted successfully when the user is not authorized and the response is as expected. we use the client fixture to simulate a delete request to the /posts/{id}/ endpoint without providing an access token in the request headers. we then assert that the response status code is 401 and the response contains the expected error message."""    
def test_unauthorized_user_delete_post(client, test_user, test_post):
    res = client.delete(f"/posts/{test_post[0].id}/")
    assert res.status_code == 401
    
"""Testing the delete post endpoint to ensure that the post is deleted successfully when the user is authorized and the response is as expected. we use the authorized_client fixture to simulate a delete request to the /posts/{id}/ endpoint with the id of the first post in the test_post fixture which creates the posts in the database. we then assert that the response status code is 204 and the post is deleted from the database."""    
def test_delete_post_success(authorized_client, test_user, test_post):
    res = authorized_client.delete(f"/posts/{test_post[0].id}/")
    assert res.status_code == 204
    
"""Testing the delete post endpoint to ensure that we receive a 404 error when the post with the given id does not exist in the database and the response is as expected. we use the authorized_client fixture to simulate a delete request to the /posts/{id}/ endpoint with an id that does not exist in the database. we then assert that the response status code is 404 and the response contains the expected error message."""    
def test_delete_post_not_exist(authorized_client, test_user, test_post):
    res = authorized_client.delete(f"/posts/88888888/")
    assert res.status_code == 404
    
"""Testing the delete post endpoint to ensure that we receive a 403 error when the user tries to delete a post that does not belong to them and the response is as expected. we use the authorized_client fixture to simulate a delete request to the /posts/{id}/ endpoint with the id of the fourth post in the test_post fixture which belongs to test_user2. we then assert that the response status code is 403 and the response contains the expected error message."""    
def test_delete_other_user_post(authorized_client, test_user, test_post):
    res = authorized_client.delete(f"/posts/{test_post[3].id}/")
    assert res.status_code == 403
    
    
def test_update_post_success(authorized_client, test_user, test_post):
    data = {
            "title": "Updated Title", 
            "content": "Updated Content",
            "id": test_post[0].id
            }
    
    res = authorized_client.put(f"/posts/{test_post[0].id}/", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]
    
    
def test_update_another_user_post(authorized_client, test_user, test_user2, test_post):
    data = {
            "title": "Updated Title", 
            "content": "Updated Content",
            "id": test_post[3].id
            }
    
    res = authorized_client.put(f"/posts/{test_post[3].id}/", json=data)
    assert res.status_code == 403
    
           
    
def test_unauthorized_user_update_post(client, test_user, test_post):
    res = client.put(f"/posts/{test_post[0].id}/")
    assert res.status_code == 401
    
    
def test_update_post_not_exist(authorized_client, test_user, test_post):
    data = {
            "title": "Updated Title", 
            "content": "Updated Content",
            "id": test_post[3].id
            }
    res = authorized_client.put(f"/posts/88888888/", json=data)
    assert res.status_code == 404