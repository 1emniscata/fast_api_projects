from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from fast_api_four_hrs.blog import schemas, models
from fast_api_four_hrs.blog.database import get_db
from fast_api_four_hrs.blog.hashing import Hash
from fast_api_four_hrs.blog.schemas import ShowUser

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)


@router.post("/", response_model=ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    # hashedPassword = pwd_cxt.hash(request.password)
    new_user = models.User(name=request.name, email=request.email,
                           password=Hash().bcrypt(request.password))
    # new_user = models.User(**request.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{user_id}", response_model=ShowUser)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        # response.status_code = status.HTTP_404_NOT_FOUND
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {user_id} is not available")
    return user
