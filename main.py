from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.schemas import UserCreate, UserResponse, RoleCreate, RoleResponse, Token
from app.crud import create_user, create_role, get_user, get_role
from app.auth import authenticate_user, create_access_token, get_current_active_user, get_password_hash
from app.dependencies import get_current_active_user
from app.models import Role, User

app = FastAPI()

ACCESS_TOKEN_EXPIRE_MINUTES = 30

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=UserResponse)
async def create_new_user(user: UserCreate):
    user_dict = user.dict()
    user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
    user_obj = User(**user_dict)
    await create_user(user_obj)
    return user_obj

@app.post("/roles/", response_model=RoleResponse)
async def create_new_role(role: RoleCreate):
    role_obj = Role(**role.dict())
    await create_role(role_obj)
    return role_obj

@app.get("/users/me/", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
