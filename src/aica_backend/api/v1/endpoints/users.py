from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ....crud import crud_user
from .. import schemas
from ... import dependencies

router = APIRouter()

@router.post('/', response_model=schemas.users.User)
def create_user_endpoint(
        user: schemas.users.UserCreate, db: Session = Depends(dependencies.get_db)
):
    db_user = crud_user.get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered.")

    return crud_user.create_user(db=db, user=user)
