"""Authentication router"""
from fastapi import APIRouter, Depends, HTTPException, Header, File, UploadFile
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth_service import (
    register_user, login_user, get_current_user
)
from app.schemas import UserRegister, UserLogin, UserResponse, UserUpdate, TokenResponse
from typing import Optional
import os
import shutil

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user
    """
    try:
        user = register_user(db, user_data)
        
        # Auto-login after registration
        from app.services.auth_service import UserLogin as LoginData
        login_data = LoginData(email=user_data.email, password=user_data.password)
        token_response = login_user(db, login_data)
        
        return token_response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


@router.post("/login", response_model=TokenResponse)
def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """
    Login with email and password
    """
    try:
        token_response = login_user(db, login_data)
        return token_response
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")


@router.get("/me", response_model=UserResponse)
def get_profile(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    """
    Get current user profile
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization token")
    
    token = authorization.replace("Bearer ", "")
    user = get_current_user(db, token)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return user


@router.put("/me", response_model=UserResponse)
def update_profile(
    update_data: UserUpdate,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Update current user profile
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization token")
    
    token = authorization.replace("Bearer ", "")
    user = get_current_user(db, token)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    # Update fields
    if update_data.full_name:
        user.full_name = update_data.full_name
    if update_data.phone_number:
        user.phone_number = update_data.phone_number
    if update_data.greenhouse_location:
        user.greenhouse_location = update_data.greenhouse_location
    if update_data.address:
        user.address = update_data.address
    
    from datetime import datetime
    user.updated_at = datetime.now()
    db.commit()
    db.refresh(user)
    
    return user


@router.post("/upload-photo")
def upload_profile_photo(
    file: UploadFile = File(...),
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """
    Upload profile photo
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization token")
    
    token = authorization.replace("Bearer ", "")
    user = get_current_user(db, token)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    # Create upload directory if not exists
    upload_dir = "app/uploads/profile_photos"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Save file with user ID as prefix
    filename = f"user_{user.id}_{file.filename}"
    filepath = os.path.join(upload_dir, filename)
    
    try:
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Update user profile photo URL
        user.profile_photo_url = f"/uploads/profile_photos/{filename}"
        db.commit()
        db.refresh(user)
        
        return {
            "message": "Photo uploaded successfully",
            "url": user.profile_photo_url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Photo upload failed: {str(e)}")
    finally:
        file.file.close()
