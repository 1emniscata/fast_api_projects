from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from fast_api_four_hrs.blog import models, schemas


def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs


def create(request: schemas.Blog, db: Session):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def delete(blog_id: int, db: Session):
    # blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    blog = db.get(models.Blog, {"id": blog_id})
    # if not blog.first():
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {blog_id} is not available")

    db.delete(blog)
    db.commit()
    return "Done"


def update(blog_id: int, request: schemas.Blog, db: Session):
    # blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    blog = db.get(models.Blog, {"id": blog_id})
    # if not blog.first():
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {blog_id} is not available")

    # blog.update(values=request.dict(), synchronize_session=False)
    db.query(models.Blog).update(values=request.dict(), synchronize_session=False)
    db.commit()
    return "updated"


def show(blog_id: int, db: Session):
    # blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    blog = db.get(models.Blog, {"id": blog_id})
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {blog_id} is not available")
    return blog