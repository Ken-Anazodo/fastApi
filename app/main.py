from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post, user, auth, vote



# models.Base.metadata.create_all(bind=engine) #This creates the tables in the database if they don't already exist. It uses the engine to connect to the database and create the tables based on the models defined in the models.py file.
app = FastAPI()

origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
        
app.include_router(post.router) # This is used to include the routes from the post router in the main app. It is used to organize the routes in different files and folders. we use the router object to split up all of our routes or path operations into seperate or different files and then we then we import them by calling app.include_router and then icluding the specifc router object of that file
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Welcome to my API. We did it!"}


