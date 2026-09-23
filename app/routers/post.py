from typing import List, Optional
from fastapi import HTTPException, status, Response, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, oauth2
from app.schemas import PostCreate, Post, PostOut
from ..database import get_db



#=========================================================================================================================================================================================================
"""USING SQLALCHEMY ORM TO INTERACT WITH THE DATABASE"""
#=========================================================================================================================================================================================================
router = APIRouter(
    prefix="/posts", #This is used to prefix all the routes in this router with /posts. it's the same as saying /posts
    tags= ["Posts"] #This is used to group all the routes in this router under the Posts tag in the documentation.
)

"""Get All Posts"""
# @router.get("/", response_model=List[Post]) #response_model=List[Post] is saying give us a list of the specific schema Post model(list of posts). it is used to tell FastAPI to use the Post schema to validate and verify the data returned from the database and return it to the client. It is used to ensure that the data returned from the database conforms to the expected structure defined in the Post schema. It stops you from returning data shouldn't be sent to the client. It ensures that only the expected data is returned to the client.
@router.get("/", response_model=List[PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""): #db is a dependency that will be used to get a database session. It will be used in the path operations to get a database session and uses it to interact with the database. skip and limit is added to handle pagination, we use limit to determine the number of item to be displayed per page and offset to determine how many item to skip before displaying the remaining items on a page.
    print(limit)
    posts = db.query(models.Post).all() # This is used to query the database and get all the posts from the posts table. It queries the Post model and gets all the posts from the database.
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all() #This is used to query the database and get all the posts from the posts table that belong to the current user.
    # posts = db.query(models.Post).limit(limit).offset(skip).all() #skip and limit is added to handle pagination, we use limit to determine the number of item to be displayed per page and offset to determine how many item to skip before displaying the remaining items on a page.
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() #To search the words entered in the items in the database and return and display those items. we use % as space in the browser or postman to show space between text 
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).limit(limit).offset(skip).all() #This is used to query the database and get all the posts from the posts table along with the number of votes for each post. It queries the Post model and gets all the posts from the database. It uses the join method to join the Vote model with the Post model on the post_id column. It uses the group_by method to group the results by the post_id column. It uses the func.count method to count the number of votes for each post. It uses the label method to label the count as "votes". It uses isouter=True to perform a left outer join, which means that it will return all posts even if they have no votes.
    print(results)
    return results


"""Search Posts"""
@router.get("/search", response_model=List[PostOut]) #response_model=List[Post] is saying give us a list of the specific schema Post model(list of posts). it is used to tell FastAPI to use the Post schema to validate and verify the data returned from the database and return it to the client. It is used to ensure that the data returned from the database conforms to the expected structure defined in the Post schema. It stops you from returning data shouldn't be sent to the client. It ensures that only the expected data is returned to the client.
def search_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""): #db is a dependency that will be used to get a database session. It will be used in the path operations to get a database session and uses it to interact with the database. skip and limit is added to handle pagination, we use limit to determine the number of item to be displayed per page and offset to determine how many item to skip before displaying the remaining items on a page and search is added to handle searching, we use search to determine the keyword to be searched in the title of the posts.
    print(limit)
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() #To search the words entered in the items in the database and return and display those items. we use % as space in the browser or postman to show space between text 
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() #This is used to query the database and get all the posts from the posts table along with the number of votes for each post. It queries the Post model and gets all the posts from the database. It uses the join method to join the Vote model with the Post model on the post_id column. It uses the group_by method to group the results by the post_id column. It uses the func.count method to count the number of votes for each post. It uses the label method to label the count as "votes". It uses isouter=True to perform a left outer join, which means that it will return all posts even if they have no votes.
    return results


"""Create Post"""
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post) #Status code is used here to replace the default status code | response_model=Post is used to tell FastAPI to use the Post schema to validate and verify the data returned from the database and return it to the client. It is used to ensure that the data returned from the database conforms to the expected structure defined in the Post schema. It stops you from returning data shouldn't be sent to the client. It ensures that only the expected data is returned to the client.
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): #PostCreate is a schema that defines, verifies and validates the type of data we receive or are expecting and PostCreate is assigned to post variable parameter. current_user is a dependecy we add from the oauth2 module, we use it to protect this route and requires a user to be Logged In to access it, we expect that the user provides an access_token which is verified before granting access to this route. we pass the access_token from the request to get_current_user for verification
    # print(post.dict(), flush=True)
    # new_post = models.Post(title=post.title, content=post.content, published=post.published) #This creates a new instance of the Post model with the data received in the request body. It uses the PostCreate schema to validate and verify the data received in the request body.
    print(current_user.id)
    print(current_user.email)
    new_post = models.Post(owner_id = current_user.id, **post.dict()) #It uses the PostCreate schema to validate and verify the data received in the request body. it uses the ** operator to unpack the dictionary returned by the post.dict() method and pass it as keyword arguments to the Post model constructor. so even if we add more fields(column) to the PostCreate schema, we don't have to change the code here, it will automatically unpack the dictionary and pass it as keyword arguments to the Post model constructor. it is the same as writing new_post = models.Post(title=post.title, content=post.content, published=post.published) but it is more flexible and scalable. it is a better way to create a new instance of the Post model with the data received inthe request body. we add the user_id seperatly because the user doesn't send the user_id as payload, since the user must be logged in to create a post, we get the user_id from the token using get_current_user and then send it to the database along with the user input from the payload 
    db.add(new_post) #This adds the new post tothe database session. It addsthe new post tothe database session but does not commit it yet.
    db.commit() #This commitsthe changes tothe database and savesthe new post tothe database.
    db.refresh(new_post) #This retrievesthe new post created and stored inthe database and stores it inthe new_post variable.
    return new_post


"""Get Post by Id"""
@router.get("/{id}", response_model=PostOut)
def get_post(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)): 
    # post = db.query(models.Post).filter(models.Post.id == id).first() #This is used to query the database and get the post with the given Id from the posts table. It queries the Post model and gets the post with the given Id from the database. It uses the filter method to filter the posts based on the given Id and returns the first post that matches the filter criteria. If no post is found, it returns None.
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first() #It returns a tuple. This is used to query the database and get the post with the given Id from the posts table along with the number of votes for that post. It queries the Post model and gets the post with the given Id from the database. It uses the join method to join the Vote model with the Post model on the post_id column. It uses the group_by method to group the results by the post_id column. It uses the func.count method to count the number of votes for that post. It uses the label method to label the count as "votes". It uses isouter=True to perform a left outer join, which means that it will return all posts even if they have no votes.
    
    if not post:
        print(f"The post with {id} as Id does not exist")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with {id} as Id does not exist")
    
    # unpack the tuple into Post object and vote count
    Post, vote = post   # ← unpack here
    
    if Post.owner_id != current_user.id: #This is used to check if the user is authorized to get the single post requested (if the single post requested belongs to the user). If the user is not authorized, it raises an HTTPException with a 403 status code and a detail message.
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to perform this action") 
        
    return post



"""Delete Post"""
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id) #This is used to query the database and get the post with the given Id from the posts table. It queries the Post model and gets the post with the given Id from the database. 
    post = post_query.first() #This is used to query the database and get the post with the given Id from the posts table. It queries the Post model and gets the post with the given Id from the database. It uses the first() method to get the first post that matches the filter criteria. If no post is found, it returns None.
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with {id} as Id does not exist")
    
    if post.owner_id != current_user.id: #This is used to check if the user is authorized to delete the post (if the post to be deleted belongs to the user). If the user is not authorized, it raises an HTTPException with a 403 status code and a detail message.
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to perform this action") 
    
    post_query.delete(synchronize_session=False) #This deletes the post with the given Id from the database. It uses the delete method to delete the post from the database. The synchronize_session=False parameter is used to prevent SQLAlchemy from synchronizing the session with the database after the delete operation. This is done to improve performance and avoid unnecessary database queries.
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT) # we don't send a message to the frontend when we delete something, we simply use Response to send a status code only
  
  
  
"""Update Post"""
@router.put("/{id}", response_model=Post)
def update_post(id:int, updated_post:PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first() #This is used to query the database and get the post with the given Id from the posts table. It queries the Post model and gets the post with the given Id from the database. It uses the first() method to get the first post that matches the filter criteria. If no post is found, it returns None.
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with {id} as Id does not exist")
    
    if post.owner_id != current_user.id: #This is used to check if the user is authorized to update the post (if the post to be updated belongs to the user). If the user is not authorized, it raises an HTTPException with a 403 status code and a detail message.
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to perform this action")
        
    post_query.update(updated_post.dict(), synchronize_session=False) #This updates the post with the given Id in the database with the new values. It uses the update method to update the post in the database. The synchronize_session=False parameter is used to prevent SQLAlchemy from synchronizing the session with the database after the update operation. This is done to improve performance and avoid unnecessary database queries.
    db.commit()
    return post_query.first() #This returns the updated post to the client. It uses the first() method to get the first post that matches the filter criteria. If no post is found, it returns None.






