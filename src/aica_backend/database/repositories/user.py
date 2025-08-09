from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import Optional
import logging

from .. import models
from ...api.v1.schemas import users as user_schemas
from ...core.security import get_password_hash, security_validator

logger = logging.getLogger(__name__)

class UserCRUD:
    """
    Enhanced CRUD operations for User model with security best practices.
    Provides centralized user management with proper validation and logging.
    """
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
        """
        Retrieve user by email with input sanitization.
        Returns None if user not found.
        """
        try:
            # Sanitize email input
            sanitized_email = security_validator.sanitize_email(email)
            
            if not sanitized_email or not security_validator.validate_email_format(sanitized_email):
                logger.warning(f"Invalid email format provided: {email}")
                return None
            
            user = db.query(models.User).filter(models.User.email == sanitized_email).first()
            
            if user:
                logger.debug(f"User found: {sanitized_email}")
            else:
                logger.debug(f"User not found: {sanitized_email}")
            
            return user
            
        except Exception as e:
            logger.error(f"Error retrieving user by email {email}: {str(e)}")
            return None
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
        """
        Retrieve user by ID with validation.
        Returns None if user not found.
        """
        try:
            if not isinstance(user_id, int) or user_id <= 0:
                logger.warning(f"Invalid user ID provided: {user_id}")
                return None
            
            user = db.query(models.User).filter(models.User.id == user_id).first()
            
            if user:
                logger.debug(f"User found by ID: {user_id}")
            else:
                logger.debug(f"User not found by ID: {user_id}")
            
            return user
            
        except Exception as e:
            logger.error(f"Error retrieving user by ID {user_id}: {str(e)}")
            return None
    
    @staticmethod
    def create_user(db: Session, user: user_schemas.UserCreate) -> Optional[models.User]:
        """
        Create new user with enhanced security validation.
        Returns created user or None if creation fails.
        """
        try:
            # Sanitize and validate email
            sanitized_email = security_validator.sanitize_email(user.email)
            
            if not security_validator.validate_email_format(sanitized_email):
                logger.warning(f"Invalid email format for user creation: {user.email}")
                raise ValueError("Invalid email format")
            
            # Check if user already exists
            existing_user = UserCRUD.get_user_by_email(db, sanitized_email)
            if existing_user:
                logger.warning(f"Attempt to create user with existing email: {sanitized_email}")
                raise ValueError("User with this email already exists")
            
            # Validate password strength
            is_valid_password, error_message = security_validator.validate_password_strength(user.password)
            if not is_valid_password:
                logger.warning(f"Weak password attempt for user: {sanitized_email}")
                raise ValueError(f"Password validation failed: {error_message}")
            
            # Hash password securely
            hashed_password = get_password_hash(user.password)
            
            # Create user model
            db_user = models.User(
                email=sanitized_email,
                hashed_password=hashed_password
            )
            
            # Save to database
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            
            logger.info(f"New user created successfully: {sanitized_email}")
            return db_user
            
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Database integrity error creating user {user.email}: {str(e)}")
            raise ValueError("User with this email already exists")
        except ValueError as e:
            db.rollback()
            logger.warning(f"Validation error creating user {user.email}: {str(e)}")
            raise e
        except Exception as e:
            db.rollback()
            logger.error(f"Unexpected error creating user {user.email}: {str(e)}")
            raise ValueError("Failed to create user")
    
    @staticmethod
    def update_user_password(db: Session, user_id: int, new_password: str) -> bool:
        """
        Update user password with security validation.
        Returns True if successful, False otherwise.
        """
        try:
            # Get user
            user = UserCRUD.get_user_by_id(db, user_id)
            if not user:
                logger.warning(f"Attempt to update password for non-existent user ID: {user_id}")
                return False
            
            # Validate new password strength
            is_valid_password, error_message = security_validator.validate_password_strength(new_password)
            if not is_valid_password:
                logger.warning(f"Weak password update attempt for user ID: {user_id}")
                raise ValueError(f"Password validation failed: {error_message}")
            
            # Hash new password
            hashed_password = get_password_hash(new_password)
            
            # Update password
            user.hashed_password = hashed_password
            db.commit()
            
            logger.info(f"Password updated successfully for user ID: {user_id}")
            return True
            
        except ValueError as e:
            db.rollback()
            logger.warning(f"Password update validation error for user ID {user_id}: {str(e)}")
            raise e
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating password for user ID {user_id}: {str(e)}")
            return False
    
    @staticmethod
    def delete_user(db: Session, user_id: int) -> bool:
        """
        Soft delete user (you might want to implement soft deletion).
        Returns True if successful, False otherwise.
        """
        try:
            user = UserCRUD.get_user_by_id(db, user_id)
            if not user:
                logger.warning(f"Attempt to delete non-existent user ID: {user_id}")
                return False
            
            # For now, we'll do a hard delete, but you might want soft deletion
            db.delete(user)
            db.commit()
            
            logger.info(f"User deleted successfully: {user.email} (ID: {user_id})")
            return True
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting user ID {user_id}: {str(e)}")
            return False
    
    @staticmethod
    def list_users(db: Session, skip: int = 0, limit: int = 100) -> list[models.User]:
        """
        List users with pagination.
        Returns list of users.
        """
        try:
            # Validate pagination parameters
            skip = max(0, skip)  # Ensure skip is not negative
            limit = min(max(1, limit), 1000)  # Ensure limit is between 1 and 1000
            
            users = db.query(models.User).offset(skip).limit(limit).all()
            
            logger.debug(f"Retrieved {len(users)} users (skip: {skip}, limit: {limit})")
            return users
            
        except Exception as e:
            logger.error(f"Error listing users: {str(e)}")
            return []

# Create global instance for backward compatibility
def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Backward compatibility function"""
    return UserCRUD.get_user_by_email(db, email)

def create_user(db: Session, user: user_schemas.UserCreate) -> Optional[models.User]:
    """Backward compatibility function"""
    return UserCRUD.create_user(db, user)