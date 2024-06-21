from fastapi import Depends, HTTPException, status
from .auth import get_current_user
from .models import User

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:  # Assuming `is_active` is an attribute of `User`
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user
