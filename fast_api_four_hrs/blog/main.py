from typing import List

from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import models
from fast_api_four_hrs.blog import schemas
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from .hashing import Hash
from .schemas import ShowUser

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=["blogs"])
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete("/blog/{blog_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["blogs"])
def delete(blog_id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {blog_id} is not available")

    blog.delete(synchronize_session=False)
    db.commit()
    return "Done"


@app.put("/blog/{blog_id}", status_code=status.HTTP_202_ACCEPTED, tags=["blogs"])
def update(blog_id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {blog_id} is not available")

    blog.update(values=request.dict(), synchronize_session=False)
    db.commit()
    return "updated"


@app.get("/blog", response_model=List[schemas.ShowBlog], tags=["blogs"])
def all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{blog_id}", status_code=200, response_model=schemas.ShowBlog, tags=["blogs"])
def show(blog_id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {blog_id} is not available")
    return blog


# pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.post("/user", response_model=ShowUser, tags=["users"])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    # hashedPassword = pwd_cxt.hash(request.password)
    new_user = models.User(name=request.name, email=request.email,
                           password=Hash().bcrypt(request.password))
    # new_user = models.User(**request.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/user/{user_id}", response_model=ShowUser, tags=["users"])
def get_user(user_id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        # response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {user_id} is not available")
    return user