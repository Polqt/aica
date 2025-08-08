import secrets
import re
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Tuple
from jose import jwt, JWTError
from passlib.context import CryptContext
from .config import settings

logger = logging.getLogger(__name__)

pwd_context = CryptContext(
    schemes=["bcrypt"], 
    deprecated="auto",
    bcrypt__rounds=12  
)

class SecurityValidator:
    @staticmethod
    def validate_password_strength(password: str) -> Tuple[bool, str]:
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if len(password) > 128:
            return False, "Password must be less than 128 characters"
        
        if not re.search(r"[A-Z]", password):
            return False, "Password must contain at least one uppercase letter"
        
        if not re.search(r"[a-z]", password):
            return False, "Password must contain at least one lowercase letter"
        
        if not re.search(r"\d", password):
            return False, "Password must contain at least one number"
        
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "Password must contain at least one special character"
        
        return True, "Password meets security requirements"
    
    @staticmethod
    def sanitize_email(email: str) -> str:
        if not email:
            return ""
        
        email = email.strip().lower()
    
        email = re.sub(r'[<>"\']', '', email)
        
        return email
    
    @staticmethod
    def validate_email_format(email: str) -> bool:
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, email))

class TokenManager:
    def __init__(self):
        self.blacklisted_tokens = set()  
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(), 
            "jti": secrets.token_urlsafe(32),  
            "type": "access"  
        })
        
        try:
            encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
            logger.info(f"Access token created for user: {data.get('sub', 'unknown')}")
            return encoded_jwt
        except Exception as e:
            logger.error(f"Token creation failed: {str(e)}")
            raise
    
    def create_refresh_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=7)  
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "jti": secrets.token_urlsafe(32),
            "type": "refresh"
        })
        
        try:
            encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
            logger.info(f"Refresh token created for user: {data.get('sub', 'unknown')}")
            return encoded_jwt
        except Exception as e:
            logger.error(f"Refresh token creation failed: {str(e)}")
            raise
    
    def verify_token(self, token: str, token_type: str = "access") -> Optional[Dict[str, Any]]:
        try:
            if self.is_token_blacklisted(token):
                logger.warning("Attempted use of blacklisted token")
                return None
            
            # Decode token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            
            # Verify token type
            if payload.get("type") != token_type:
                logger.warning(f"Token type mismatch. Expected: {token_type}, Got: {payload.get('type')}")
                return None
            
            return payload
            
        except jwt.ExpiredSignatureError:
            logger.warning("Token has expired")
            return None
        except JWTError as e:
            logger.warning(f"Token verification failed: {str(e)}")
            return None
    
    def blacklist_token(self, token: str):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            jti = payload.get("jti")
            if jti:
                self.blacklisted_tokens.add(jti)
                logger.info(f"Token blacklisted: {jti}")
            else:
                # If no JTI, blacklist the token directly
                self.blacklisted_tokens.add(token)
                logger.info(f"Token blacklisted directly: {token[:20]}...")
        except JWTError:
            # If we can't decode the token, add it directly
            self.blacklisted_tokens.add(token)
            logger.info(f"Token blacklisted directly (invalid): {token[:20]}...")
    
    def is_token_blacklisted(self, token: str) -> bool:
        try:
            # Check direct token blacklist
            if token in self.blacklisted_tokens:
                return True
            
            # Check JTI blacklist
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            jti = payload.get("jti")
            if jti and jti in self.blacklisted_tokens:
                return True
                
            return False
        except JWTError:
            return True

token_manager = TokenManager()
security_validator = SecurityValidator()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        logger.error(f"Password verification failed: {str(e)}")
        return False

def get_password_hash(password: str) -> str:
    is_valid, error_message = security_validator.validate_password_strength(password)
    if not is_valid:
        raise ValueError(f"Password validation failed: {error_message}")
    
    try:
        return pwd_context.hash(password)
    except Exception as e:
        logger.error(f"Password hashing failed: {str(e)}")
        raise

def create_access_token(data: dict) -> str:
    return token_manager.create_access_token(data)

def generate_secure_random_string(length: int = 32) -> str:
    return secrets.token_urlsafe(length)
