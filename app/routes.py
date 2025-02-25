from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserLogin, UserResponse
from app.auth import get_password_hash, verify_password, create_access_token
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = APIRouter()

templates = Jinja2Templates(directory="app/frontend/templates/")
print(templates)

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")
    
    existing_username = db.query(User).filter(User.username == user_data.username).first()
    if existing_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already in use")

    try:
        hashed_pw = get_password_hash(user_data.password)
        new_user = User(username=user_data.username, email=user_data.email, password=hashed_pw)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
    except Exception as ex:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(ex))

@router.get('/register', response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("index2.html", {"request": request})


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/login", response_model=UserResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_data.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong email or password")
    
    # Verify the provided password against the hashed password in the database
    if not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Wrong email or password")
    
    
    access_token = create_access_token(data={"sub": user.email}, expires_delta=300)  # `sub` is a standard claim representing the subject (email)

    # Return the user details and the access token
    return {"id": user.id, "username": user.username, "email": user.email}



