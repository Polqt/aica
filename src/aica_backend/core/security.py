import secrets
import re

from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
from jose import jwt, JWTError
from passlib.context import CryptContext
from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)

class SecurityValidator:
    """Handles password and email validation with security best practices."""

    @staticmethod
    def validate_password_strength(password: str) -> Tuple[bool, str]:
        """Validate password meets security requirements."""
        if len(password) < settings.MIN_PASSWORD_LENGTH:
            return False, f"Password must be at least {settings.MIN_PASSWORD_LENGTH} characters long"
        
        if len(password) > settings.MAX_PASSWORD_LENGTH:
            return False, f"Password must be less than {settings.MAX_PASSWORD_LENGTH} characters"
        
        if not re.search(r"[A-Z]", password):
            return False, "Password must contain at least one uppercase letter"
        
        if not re.search(r"[a-z]", password):
            return False, "Password must contain at least one lowercase letter"
        
        if not re.search(r"\d", password):
            return False, "Password must contain at least one number"
        
        if settings.REQUIRE_SPECIAL_CHARS and not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "Password must contain at least one special character"
        
        return True, "Password meets security requirements"
    
    @staticmethod
    def sanitize_email(email: str) -> str:
        """Sanitize email address for security."""
        if not email:
            return ""
        
        email = email.strip().lower()
        return re.sub(r'[<>"\']', '', email)
    
    @staticmethod
    def validate_email_format(email: str) -> bool:
        """Validate email format using regex."""
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, email))


class TokenManager:
    """Handles JWT token creation, validation, and blacklisting."""

    def __init__(self):
        self.blacklisted_tokens = set()
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create a new access token."""
        to_encode = data.copy()
        
        expire = (datetime.utcnow() + expires_delta) if expires_delta else \
                 (datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "jti": secrets.token_urlsafe(32),
            "type": "access"
        })
        
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    def create_refresh_token(self, data: dict) -> str:
        """Create a new refresh token."""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "jti": secrets.token_urlsafe(32),
            "type": "refresh"
        })
        
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    def verify_token(self, token: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
        """Verify and decode a JWT token."""
        try:
            if self.is_token_blacklisted(token):
                return None
            
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            
            if payload.get("type") != token_type:
                return None
            
            return payload
            
        except (jwt.ExpiredSignatureError, JWTError):
            return None
    
    def blacklist_token(self, token: str) -> None:
        """Add token to blacklist."""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            jti = payload.get("jti")
            if jti:
                self.blacklisted_tokens.add(jti)
            else:
                self.blacklisted_tokens.add(token)
        except JWTError:
            self.blacklisted_tokens.add(token)
    
    def is_token_blacklisted(self, token: str) -> bool:
        """Check if token is blacklisted."""
        try:
            if token in self.blacklisted_tokens:
                return True
            
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            jti = payload.get("jti")
            return jti in self.blacklisted_tokens if jti else False
                
        except JWTError:
            return True


# Global instances
token_manager = TokenManager()
security_validator = SecurityValidator()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """Hash a password with validation."""
    is_valid, error_message = security_validator.validate_password_strength(password)
    if not is_valid:
        raise ValueError(f"Password validation failed: {error_message}")
    
    return pwd_context.hash(password)


def create_access_token(data: dict) -> str:
    """Create access token (legacy function for backward compatibility)."""
    return token_manager.create_access_token(data)


def generate_secure_random_string(length: int = 32) -> str:
    """Generate a secure random string."""
    return secrets.token_urlsafe(length)
