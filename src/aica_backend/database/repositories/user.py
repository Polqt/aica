from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional

from .. import models
from ...api.v1.schemas import users as user_schemas
from ...core.security import get_password_hash, security_validator


class UserCRUD:
    """Enhanced CRUD operations for User model with security best practices."""
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
        """Retrieve user by email with input sanitization."""
        try:
            sanitized_email = security_validator.sanitize_email(email)
            
            if not sanitized_email or not security_validator.validate_email_format(sanitized_email):
                return None
            
            return db.query(models.User).filter(models.User.email == sanitized_email).first()
            
        except Exception:
            return None
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
        """Retrieve user by ID with validation."""
        try:
            if not isinstance(user_id, int) or user_id <= 0:
                return None
            
            return db.query(models.User).filter(models.User.id == user_id).first()
            
        except Exception:
            return None
    
    @staticmethod
    def create_user(db: Session, user: user_schemas.UserCreate) -> Optional[models.User]:
        """Create new user with enhanced security validation."""
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
                hashed_password=hashed_password
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
            db.rollback()
            raise ValueError("Failed to create user")
    
    @staticmethod
    def update_user_password(db: Session, user_id: int, new_password: str) -> bool:
        """Update user password with security validation."""
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
        """Delete user (hard delete for now, consider soft deletion for production)."""
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
    
    @staticmethod
    def list_users(db: Session, skip: int = 0, limit: int = 100) -> list[models.User]:
        """List users with pagination."""
        try:
            skip = max(0, skip)
            limit = min(max(1, limit), 1000)
            
            return db.query(models.User).offset(skip).limit(limit).all()
            
        except Exception:
            return []


# Backward compatibility functions
def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Backward compatibility function"""
    return UserCRUD.get_user_by_email(db, email)


def create_user(db: Session, user: user_schemas.UserCreate) -> Optional[models.User]:
    """Backward compatibility function"""
    return UserCRUD.create_user(db, user)