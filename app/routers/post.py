from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, oauth2
from ..database import engine,  get_db
from ..utils import hash
from ..schemas import Post, PostResponse
from sqlalchemy import func


from typing import Optional, List

router = APIRouter(
    prefix="/post",
    tags=["Posts"]
)


#response_model=List[PostResponse]
@router.get("/")
def get_posts(db:Session = Depends(get_db), current_user = Depends(oauth2.get_current_user),limit:int = 10):
    #cursor.execute("SELECT * FROM posts")
    posts =  post =  db.query(models.Post).limit(limit).all()
    #print(posts)
    # results = db.query(models.Post, func.count(models.Votes.post_id).label('votes')).join(models.Votes, models.Votes.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    # print('join count begin')
    # print(results)
    # print('join count end ')
    return posts

@router.post('/',status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_posts(post: Post, response: Response, db:Session = Depends(get_db), current_user  = Depends(oauth2.get_current_user)):
    new_posts = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_posts)
    db.commit()
    db.refresh(new_posts)
    return new_posts


@router.get('/{id}')
def get_posts(id: int, response: Response, db:Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id}")
    return  post
 

 