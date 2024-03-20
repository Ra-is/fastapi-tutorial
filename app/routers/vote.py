from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, oauth2
from ..database import engine,  get_db
from ..utils import hash
from ..schemas import Vote

router = APIRouter(
     prefix="/vote",
    tags=["Vote"]
)

@router.post('/',status_code=status.HTTP_201_CREATED)
def vote(vote: Vote, db:Session = Depends(get_db), current_user  = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
         raise HTTPException(status_code=status.HTTP_404_CONFLICT, detail="Post does not exist")

    vote_query =  db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
       if found_vote:
         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Current user has already voted")
       new_votes = models.Votes(post_id = vote.post_id, user_id = current_user.id) 
       db.add(new_votes)
       db.commit()
       return {"message": "Success"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Vote does not exist")

        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Deleted Votes"}

   
