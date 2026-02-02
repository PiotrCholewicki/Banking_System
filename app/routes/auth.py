from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.auth.auth import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_current_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from app.database import get_session
from app.models.client import Client
from app.models.user import User
from app.routes.clients import delete_client
from app.schemas.auth import UserRegister, Token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, session: Session = Depends(get_session)):

    # simple validation
    if not payload.username or not payload.password or len(payload.password) < 4:
        raise HTTPException(status_code=400, detail="Invalid credentials (min 4 chars)")

    # unique username
    existing = session.exec(
        select(User).where(User.username == payload.username)
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Username already exists")

    # Create user
    user = User(
        username=payload.username,
        hashed_password=get_password_hash(payload.password),
        role="client",
        is_active=True,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    # Create client
    client = Client(
        name=user.username,
        balance=payload.balance,
    )
    session.add(client)
    session.commit()
    session.refresh(client)

    user.client_id = client.id
    session.add(user)
    session.commit()
    session.refresh(user)

    # return token for swagger
    token = create_access_token(
        data={"sub": user.username},
        role=user.role,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=token)


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):

    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=token)


@router.get("/me", response_model=User)
def me(current_user: User = Depends(get_current_user)):
    return current_user


@router.delete("/delete/", status_code=204)
def delete_user(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    if current_user.role == "admin":
        raise HTTPException(status_code=400, detail="Can't delete admin")
    delete_client(current_user.client_id, session)
    session.delete(current_user)
    session.commit()
    return Response(status_code=204)
