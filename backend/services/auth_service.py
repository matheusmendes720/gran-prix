from datetime import datetime, timedelta
from typing import Optional
import jwt
import os
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy import text

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'change-this-in-production')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 * 24 * 60  # 30 days


class AuthService:
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against a hashed password"""
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Hash a password using bcrypt"""
        return pwd_context.hash(password)
    
    def authenticate_user(self, username: str, password: str) -> Optional[dict]:
        """Authenticate user and return user info if valid"""
        query = text("""
            SELECT user_id, username, email, password_hash, role, active, last_login
            FROM support.users 
            WHERE username = :username AND active = true
        """)
        
        result = self.db.execute(query, {"username": username})
        user = result.fetchone()
        
        if not user or not self.verify_password(password, user.password_hash):
            return None
        
        # Update last login
        update_query = text("UPDATE support.users SET last_login = NOW() WHERE user_id = :user_id")
        self.db.execute(update_query, {"user_id": user.user_id})
        self.db.commit()
        
        return {
            "user_id": user.user_id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        }
    
    def create_access_token(self, user_id: int, role: str) -> str:
        """Create a new access token with user information"""
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        expire = datetime.utcnow() + expires_delta
        
        payload = {
            "user_id": user_id,
            "role": role,
            "exp": expire,
            "iat": datetime.utcnow()
        }
        
        encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str) -> Optional[dict]:
        """Verify a token and return user info"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: int = payload.get("user_id")
            role: str = payload.get("role")
            
            if user_id is None or role is None:
                return None
                
            # Verify that user is still active
            query = text("SELECT user_id, username, role, active FROM support.users WHERE user_id = :user_id AND active = true")
            result = self.db.execute(query, {"user_id": user_id})
            user = result.fetchone()
            
            if not user:
                return None
            
            return {
                "user_id": user.user_id,
                "username": user.username,
                "role": user.role
            }
        except jwt.PyJWTError:
            return None
    
    def get_current_user_role(self, token: str) -> Optional[str]:
        """Get the role from the token"""
        user_info = self.verify_token(token)
        return user_info.get("role") if user_info else None
    
    def check_permission(self, token: str, required_role: str) -> bool:
        """Check if user has required role/permission"""
        user_role = self.get_current_user_role(token)
        if not user_role:
            return False
        
        # Define role hierarchy: ADMIN > ANALYST > VIEWER
        role_hierarchy = {
            'ADMIN': 3,
            'ANALYST': 2,
            'VIEWER': 1
        }
        
        required_level = role_hierarchy.get(required_role, 0)
        user_level = role_hierarchy.get(user_role, 0)
        
        return user_level >= required_level

# Create a global auth service instance
# Note: This would be initialized with a specific DB session when used
def get_auth_service(db_session: Session) -> AuthService:
    """Factory function to create an auth service with a database session"""
    return AuthService(db_session)