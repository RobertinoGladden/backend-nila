"""Authentication and JWT token management"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.models import User, UserAuth
from app.schemas import UserRegister, UserLogin, TokenResponse
import os

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """Create JWT refresh token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[dict]:
    """Verify JWT token and return payload"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            return None
        return payload
    except JWTError:
        return None


def register_user(db: Session, user_data: UserRegister) -> User:
    """Register new user"""
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise ValueError("Email already registered")
    
    # Create user
    new_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        phone_number=user_data.phone_number,
        greenhouse_location=user_data.greenhouse_location,
        address=user_data.address,
    )
    db.add(new_user)
    db.flush()  # Get the user ID without committing
    
    # Create auth record
    user_auth = UserAuth(
        user_id=new_user.id,
        password_hash=hash_password(user_data.password)
    )
    db.add(user_auth)
    db.commit()
    db.refresh(new_user)
    
    return new_user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate user by email and password"""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    
    user_auth = db.query(UserAuth).filter(UserAuth.user_id == user.id).first()
    if not user_auth:
        return None
    
    if not verify_password(password, user_auth.password_hash):
        return None
    
    return user


def login_user(db: Session, login_data: UserLogin) -> TokenResponse:
    """Authenticate user and return tokens"""
    user = authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise ValueError("Invalid email or password")
    
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer"
    )


def get_current_user(db: Session, token: str) -> Optional[User]:
    """Get current user from token"""
    payload = verify_token(token)
    if payload is None:
        return None
    
    user_id: int = int(payload.get("sub"))
    user = db.query(User).filter(User.id == user_id).first()
    return user
