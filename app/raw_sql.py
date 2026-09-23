from fastapi import FastAPI, HTTPException, status, Response
import psycopg2
import time
from app.schemas import PostCreate
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine
from .routers import post, user, auth
from app.config import settings


models.Base.metadata.create_all(bind=engine) #This creates the tables in the database if they don't already exist. It uses the engine to connect to the database and create the tables based on the models defined in the models.py file.
app = FastAPI()
    

"""CONNECTION TO THE DATABASE USING PSYCOPG2 WITH RAW SQL QUERIES"""
while True:  #We use the while loop to keep trying to connect the server to the database if and when there is an error while connecting...
    try:
        conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="12345", cursor_factory=RealDictCursor) #is a Driver that only knows how to send raw SQL strings to PostgreSQL and return the data as basic Python tuples or dictionaries.
        # conn = psycopg2.connect(host=settings.database_host, database=settings.database_name, user=settings.database_username, password=settings.database_password, cursor_factory=RealDictCursor) #is a Driver that only knows how to send raw SQL strings to PostgreSQL and return the data as basic Python tuples or dictionaries.
        cursor = conn.cursor() # a database object used to execute SQL queries and fetch the resulting rows from the database. Think of a database connection as a phone call to the database server, and the cursor as the person talking on the phone, sending commands and bringing back the answers.
        print("Database connection was successful")
        break # if connection is successful, it breaks the loop and stops trying to connect since it has connected successfully..
    except Exception as error:
        print("connecting to database failed")
        print("Error: ", error)
        time.sleep(2) # if the code fails to connect, it tries to reconnect after 2 seconds...
        
        
#============================================================================================================================================
"""USING RAW SQL QUERIES TO INTERACT WITH THE DATABASE"""
#============================================================================================================================================
        
app.include_router(post.router) # This is used to include the routes from the post router in the main app. It is used to organize the routes in different files and folders. we use the router object to split up all of our routes or path operations into seperate or different files and then we then we import them by calling app.include_router and then icluding the specifc router object of that file
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Welcome to my API"}


"""Get All Posts"""
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall() # This fetches all the posts from the database and returns them to the client. It uses the cursor to execute a SQL query that selects all the posts from the posts table and fetches them using the fetchall() method. The fetched posts are then returned to the client in a JSON format.
    print(posts)
    return {"data": posts}


"""Create Post"""
@app.post("/posts", status_code=status.HTTP_201_CREATED) #Status code is used here to replace the default status code
def create_post(post:PostCreate): #Post is a schema that defines, verifies and validates the type of data we receive or are expecting and Post is assigned to post variable parameter
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published)) # %s is a placeholder used to represent a string value that will be dynamically inserted into the query at runtime
    conn.commit() # We use conn.commit() to save our changes to the database 
    new_post = cursor.fetchone() # This fetches the newly created post from the database and returns it to the client
    return {"message": "Post created successfully!", "payload": new_post}

"""Get Post by Id"""
@app.get("/posts/{id}")
def get_post(id:int):
    # post = find_post(id)
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone() # This fetches the post with the given Id from the database and returns it to the client. It uses the cursor to execute a SQL query that selects the post with the given Id from the posts table and fetches it using the fetchone() method. The fetched post is then returned to the client in a JSON format.
    if not post:
        print(f"The post with {id} as Id does not exist")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with {id} as Id does not exist")
    return {"message": "Post retrieved successfully!", "payload": post}


"""Delete Post"""
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id), ))
    deleted_post = cursor.fetchone()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with {id} as Id does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT) # we don't send a message to the frontend when we delete something, we simply use Response to send a status code only
  
    
"""Update Post"""
@app.put("/posts/{id}")
def update_post(id:int, post:PostCreate):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with {id} as Id does not exist")
    return {"message": "Post updated successfully!", "payload": updated_post}


# %s denotes a string
# %d denotes an integer
#%c denotes ASCII code representation