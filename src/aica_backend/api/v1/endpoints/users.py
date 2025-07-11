from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ....core.security import create_access_token
from ....crud import crud_user
from .. import schemas
from ... import dependencies
from ..schemas.token import Token

router = APIRouter()

@router.post('/', response_model=Token)
def create_user_endpoint(
        user: schemas.users.UserCreate, db: Session = Depends(dependencies.get_db)
):
    db_user = crud_user.get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered.")

    new_user = crud_user.create_user(db=db, user=user)

    access_token = create_access_token(data={"sub": new_user.email})

    return {"access_token": access_token, "token_type": "bearer"}
