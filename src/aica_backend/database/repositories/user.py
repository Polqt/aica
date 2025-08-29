from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional

from .. import models
from ...api.v1.schemas import users as user_schemas
from ...core.security import get_password_hash, security_validator


class UserCRUD:
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
        try:
            sanitized_email = security_validator.sanitize_email(email)
            
            if not sanitized_email or not security_validator.validate_email_format(sanitized_email):
                return None
            
            return db.query(models.User).filter(models.User.email == sanitized_email).first()
            
        except Exception:
            return None
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
        try:
            if not isinstance(user_id, int) or user_id <= 0:
                return None
            
            return db.query(models.User).filter(models.User.id == user_id).first()
            
        except Exception:
            return None
    
    @staticmethod
    def create_user(db: Session, user: user_schemas.UserCreate) -> Optional[models.User]:
        try:
            sanitized_email = security_validator.sanitize_email(user.email)
            
            if not security_validator.validate_email_format(sanitized_email):
                raise ValueError("Invalid email format")
            
            existing_user = UserCRUD.get_user_by_email(db, sanitized_email)
            if existing_user:
                raise ValueError("User with this email already exists")
            
            is_valid_password, error_message = security_validator.validate_password_strength(user.password)
            if not is_valid_password:
                raise ValueError(f"Password validation failed: {error_message}")
            
            hashed_password = get_password_hash(user.password)
            
            db_user = models.User(
                email=sanitized_email,
                hashed_password=hashed_password,
            )
            
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            
            return db_user
            
        except IntegrityError:
            db.rollback()
            raise ValueError("User with this email already exists")
        except ValueError:
            db.rollback()
            raise
    
    @staticmethod
    def update_user_password(db: Session, user_id: int, new_password: str) -> bool:
        try:
            user = UserCRUD.get_user_by_id(db, user_id)
            if not user:
                return False
            
            is_valid_password, error_message = security_validator.validate_password_strength(new_password)
            if not is_valid_password:
                raise ValueError(f"Password validation failed: {error_message}")
            
            hashed_password = get_password_hash(new_password)
            user.hashed_password = hashed_password
            db.commit()
            
            return True
            
        except ValueError:
            db.rollback()
            raise
        except Exception:
            db.rollback()
            return False
    
    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        try:
            user = UserCRUD.get_user_by_id(db, user_id)
            if not user:
                return False
            
            db.delete(user)
            db.commit()
            return True
            
        except Exception:
            db.rollback()
            return False
    