from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class Token(BaseModel):
    """Schema for authentication token response"""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: Optional[int] = Field(None, description="Token expiration time in seconds")

class TokenData(BaseModel):
    """Schema for token payload data"""
    email: EmailStr = Field(..., description="User email from token")

class RefreshToken(BaseModel):
    """Schema for refresh token"""
    refresh_token: str = Field(..., description="JWT refresh token")

class TokenResponse(BaseModel):
    """Enhanced token response with additional metadata"""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Access token expiration time in seconds")
    refresh_token: Optional[str] = Field(None, description="JWT refresh token")
    scope: str = Field(default="read write", description="Token scope")

class TokenVerification(BaseModel):
    """Schema for token verification response"""
    valid: bool = Field(..., description="Whether the token is valid")
    email: Optional[str] = Field(None, description="User email if token is valid")
    expires_at: Optional[str] = Field(None, description="Token expiration timestamp")

class TokenBlacklist(BaseModel):
    """Schema for token blacklist requests"""
    token: str = Field(..., description="Token to blacklist")
    reason: Optional[str] = Field(None, description="Reason for blacklisting")
