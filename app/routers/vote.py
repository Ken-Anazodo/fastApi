from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, database, oauth2, schemas

router = APIRouter(
    prefix="/vote", #This is used to prefix all the routes in this router with /vote. it's the same as saying /vote.
    tags=["Votes"] # This is used to group all the routes in this router under the Votes tag in the documentation.
)

@router.post("/", status_code=status.HTTP_201_CREATED) #This is used to create a new vote. It is a POST request because we are creating a new resource. We use status_code=status.HTTP_201_CREATED to indicate that the resource was created successfully.
def vote(vote:schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    posts = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {vote.post_id} does not exist")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id) # builds a query that looks for a vote in the votes table where both post_id AND user_id match. Both conditions must be true together because a vote is uniquely identified by the combination of which post and which user — the same user can vote on many posts, and the same post can be voted on by many users, but each user can only have one vote per post.
    found_vote = vote_query.first() # executes the query and returns the first matching vote, or None if no vote exists. We store the query separately from the result (vote_query vs found_vote) because we need the query object later to delete the vote if needed — vote_query.delete() — not just the result.
    
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted on post {vote.post_id}")
        
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote added successfully"}   
    
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"vote does not exist")
        vote_query.delete(synchronize_session=False)
        
        db.commit()
        return {"message": "Vote removed successfully"}
