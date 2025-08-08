from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    """Base user schema with common fields"""
    email: EmailStr = Field(..., description="User's email address")

class UserCreate(UserBase):
    """Schema for user registration"""
    password: str = Field(
        ..., 
        min_length=8, 
        max_length=128,
        description="User's password (8-128 characters)"
    )
    
    @validator('password')
    def validate_password_complexity(cls, v):
        """Validate password meets complexity requirements"""
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one number')
        if not any(c in '!@#$%^&*(),.?":{}|<>' for c in v):
            raise ValueError('Password must contain at least one special character')
        return v

class UserResponse(UserBase):
    """Schema for user data in responses (excludes sensitive info)"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class User(UserBase):
    """Full user schema (for internal use)"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class PasswordChange(BaseModel):
    """Schema for password change requests"""
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(
        ..., 
        min_length=8, 
        max_length=128,
        description="New password (8-128 characters)"
    )
    
    @validator('new_password')
    def validate_new_password_complexity(cls, v):
        """Validate new password meets complexity requirements"""
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one number')
        if not any(c in '!@#$%^&*(),.?":{}|<>' for c in v):
            raise ValueError('Password must contain at least one special character')
        return v

class UserUpdate(BaseModel):
    """Schema for user profile updates"""
    email: Optional[EmailStr] = Field(None, description="Updated email address")
    
class UserLogin(BaseModel):
    """Schema for login requests"""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")