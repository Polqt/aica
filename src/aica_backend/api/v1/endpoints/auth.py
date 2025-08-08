from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ....crud import crud_user
from ....core.security import create_access_token, verify_password
from ....core.config import settings
from .. import schemas
from ... import dependencies

router = APIRouter()

@router.post('/login/access-token', response_model=schemas.token.Token)
def login_for_access_token(
    request: Request,
    response: Response,
    db: Session = Depends(dependencies.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    if hasattr(request.app.state, 'limiter'):
        request.app.state.limiter.limit("5/minute")(request)
    
    user = crud_user.get_user_by_email(db, email=form_data.username)
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    
    # Set secure httpOnly cookie instead of returning token in response body
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  
        httponly=True,  #
        secure=settings.ENVIRONMENT == "production",  
        samesite="strict",  
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post('/logout')
def logout(response: Response):
    """
    Logout endpoint that clears the secure httpOnly cookie.
    """
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=settings.ENVIRONMENT == "production",
        samesite="strict",
    )
    return {"message": "Successfully logged out"}