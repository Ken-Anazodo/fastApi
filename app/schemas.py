from datetime import datetime
from re import U
from typing import Optional, Annotated
from pydantic import BaseModel, EmailStr, Field
# from pydantic.types import conint


"""Schema uses Pydantic to define the structure of the data that we expect to receive in the request body when creating a new post. 
It also defines the data types of the fields and whether they are required or optional. The schema is used in the create_post and 
update_post path operations to validate the incoming request data and ensure that it conforms to the expected structure. """


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None
 
"""We used in Request(create_post)"""   
class PostCreate(PostBase):
    pass


"""We used in Response(create_post, update_post, search_post)"""
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int # This is used to store the id of the user who created the post. It is a foreign key that references the id column in the users table. It is used to associate the post with the user who created it.
    owner: UserOut 
    
    class Config:# It's needed to convert the SQLAlchemy models to Pydantic models and vice versa. It is used to enable the use of the SQLAlchemy models in the path operations and return them as JSON responses.
        orm_mode = True #This is used to tell Pydantic to treat the SQLAlchemy models as dictionaries. It is used to convert the SQLAlchemy models to Pydantic models and vice versa. It is used to enable the use of the SQLAlchemy models in the path operations and return them as JSON responses.
  
  
"""We used in Response(get_posts and get_post)"""        
class PostOut(BaseModel):
    Post: Post
    votes: int
    
    class Config:
        orm_mode = True
 
         
"""We used in Request"""      
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72) #This is used to validate the password field. It is used to ensure that the password is at least 8 characters long and at most 72 characters long. It is used to prevent weak passwords and ensure that the password is strong enough to protect the user's account.   
 
    
"""We used in Response"""  
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True
        
        
"""We used in Request"""
class UserLogin(BaseModel):
    email: EmailStr
    password: str
 
 
"""We used in Response"""   
class Token(BaseModel):
    access_token: str
    token_type: str
    
    
"""We used in verify_access_token"""
class TokenData(BaseModel):
    id: Optional[str] #Optional is used to indicate that the id field is optional. It is used to allow the TokenData model to be used in situations where the id field may not be present, such as when the token is invalid or expired. It is used to prevent validation errors when the id field is not present in the token data.
    
    
class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(le=1, ge=0)] #le means less than or equal to 1 and ge means greater than or equal to 0. This is used to validate the dir field. It is used to ensure that the dir field is either 0 or 1. It is used to prevent invalid values from being passed in the request body. int ensures that the value is an integer.