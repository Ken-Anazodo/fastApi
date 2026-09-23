from sqlalchemy import Column, Integer, String, Boolean, text, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base #Base is imported from the database.py file. It is the base class that we'll use to create our models. The models are going to be extending the base class.

class Post(Base):
    __tablename__ = "posts" #This is the name of the table in the database

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default='True')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')) #This is the default value for the created_at column. It is set to the current timestamp when a new row is inserted into the table.
    owner_id =  Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False) #users in "users.id" refers to the table name of the Model User
    
    owner = relationship("User") #relationship isn't a foreign key, it does nothing in the database, It tells sqlalchemy to fetch users information from the User(model) or table based of the relationship. This is used to get the user who owns the post. This creates a relationship between the Post and User models. It is a one-to-many relationship. One user can have many posts. But one post can only belong to one user.
      

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True) #This is the email column. It is set to be unique so that no two users can have the same email address.
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')) #This is the default value for the created_at column. It is set to the current timestamp when a new row is inserted into the table.
    phone_numbers = Column(String, nullable=True)
    
class Vote(Base):
    __tablename__ = "votes"
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True) #This is the user_id column. It is a foreign key that references the id column in the users table. It is set to be a primary key so that no two votes can have the same user_id and post_id combination.
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True) #This is the post_id column. It is a foreign key that references the id column in the posts table. It is set to be a primary key so that no two votes can have the same user_id and post_id combination.