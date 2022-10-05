from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from fast_api_four_hrs.blog import schemas, models
from fast_api_four_hrs.blog.database import get_db
from fast_api_four_hrs.blog.hashing import Hash
from fast_api_four_hrs.blog.token import  create_access_token

router = APIRouter(tags=["Authentication"])


@router.post("/login")
def login(request: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):
    # user = db.query(models.User).filter(models.User.email == request.username).first()
    user = db.query(models.User).where(models.User.email == request.username).first()
    if not user:
        # # response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Invalid credentials")
    if not Hash().verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Incorrect password")
    # return user

    # return "login"
    # access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}
