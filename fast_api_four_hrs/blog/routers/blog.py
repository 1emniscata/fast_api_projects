from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from fast_api_four_hrs.blog import schemas, models
from fast_api_four_hrs.blog.database import get_db
from fast_api_four_hrs.blog.oauth2 import get_current_user
from fast_api_four_hrs.blog.repository import blog

router = APIRouter(
    prefix="/blog",
    tags=["Blogs"]
)


@router.get("/", response_model=List[schemas.ShowBlog])
def all_blogs(db: Session = Depends(get_db),
              current_user: schemas.User = Depends(get_current_user)):
    # blogs = db.query(models.Blog).all()
    # return blogs
    return blog.get_all(db)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db),
           current_user: schemas.User = Depends(get_current_user)):
    # new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    # db.add(new_blog)
    # db.commit()
    # db.refresh(new_blog)
    # return new_blog
    return blog.create(request, db)


@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT,
               )
def delete(blog_id, db: Session = Depends(get_db),
           current_user: schemas.User = Depends(get_current_user)):
    # blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    # if not blog.first():
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"Blog with the id {blog_id} is not available")
    #
    # blog.delete(synchronize_session=False)
    # db.commit()
    # return "Done"
    return blog.delete(blog_id, db)


@router.put("/{blog_id}", status_code=status.HTTP_202_ACCEPTED)
def update(blog_id, request: schemas.Blog, db: Session = Depends(get_db),
           current_user: schemas.User = Depends(get_current_user)):
    # blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
    # if not blog.first():
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"Blog with the id {blog_id} is not available")
    #
    # blog.update(values=request.dict(), synchronize_session=False)
    # db.commit()
    # return "updated"
    return blog.update(blog_id, request, db)


@router.get("/{blog_id}", status_code=200, response_model=schemas.ShowBlog)
def show(blog_id, db: Session = Depends(get_db),
         current_user: schemas.User = Depends(get_current_user)):
    # blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    # if not blog:
    #     # response.status_code = status.HTTP_404_NOT_FOUND
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"Blog with the id {blog_id} is not available")
    # return blog
    return blog.show(blog_id, db)
