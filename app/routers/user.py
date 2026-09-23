from fastapi import HTTPException, status, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, utils
from app.schemas import UserCreate, UserOut
from ..database import get_db

#=========================================================================================================================================================================================================
"""USING SQLALCHEMY ORM TO INTERACT WITH THE DATABASE"""
#=========================================================================================================================================================================================================

router = APIRouter(
    prefix="/users", #This is used to prefix all the routes in this router with /users. it's the same as saying /user\
    tags=["Users"] # This is used to group all the routes in this router under the Users tag in the documentation.
)

"""Get Users"""
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password) #This hashes the password received in the request body before storing it in the database.
    user.password = hashed_password #This replaces the plain text password received in the request body with the hashed password before storing it in the database making it more secure and preventing it from being compromised.
    
    new_user = models.User(**user.dict()) #This creates a new instance of the User model with the data received in the request body. It uses the UserCreate schema to validate and verify the data received in the request body. it uses the ** operator to unpack the dictionary returned by the user.dict() method and pass it as keyword arguments to the User model constructor. so even if we add more fields(column) to the UserCreate schema, we don't have to change the code here, it will automatically unpack the dictionary and pass it as keyword arguments to the User model constructor. it is the same as writing new_user = models.User(email=user.email, password=user.password) but it is more flexible and scalable. it is a better way to create a new instance of the User model with the data received in the request body.
    db.add(new_user) #This adds the new user tothe database session. It addsthe new user tothe database session but does not commit it yet.
    db.commit()
    db.refresh(new_user) #This retrieves the new user created and stored inthe database and stores it inthe new_user variable.
    return new_user


"""Get a User by Id"""
@router.get("/{id}/", response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The user with {id} as Id does not exist")
    
    return user