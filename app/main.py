import os
from contextlib import asynccontextmanager
from sqlite3 import IntegrityError

from dotenv import load_dotenv
from fastapi import FastAPI
from sqlmodel import SQLModel, Session, select

from app.auth.auth import get_password_hash
from app.database import engine
from app.models.user import User

from app.routes.clients import router as clients_router
from app.routes.transactions import router as transactions_router
from app.routes.transfers import router as transfers_router
from app.routes.auth import router as auth_router
from app.routes.admin import router as admin_router

# app = FastAPI()
# @app.on_event("startup")
# def on_startup():
#     SQLModel.metadata.create_all(engine)
from fastapi_pagination import add_pagination

load_dotenv()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


def seed_admin():
    with Session(engine) as session:
        existing = session.exec(
            select(User).where(User.username == ADMIN_USERNAME)
        ).first()
        if existing:
            return  # admin already exists

        admin = User(
            username=ADMIN_USERNAME,
            hashed_password=get_password_hash(ADMIN_PASSWORD),
            role="admin",
            is_active=True,
            client_id=None,
        )
        session.add(admin)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()


@asynccontextmanager
async def lifespan(app: FastAPI):

    SQLModel.metadata.create_all(engine)
    seed_admin()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(admin_router)
app.include_router(auth_router)
app.include_router(clients_router)
app.include_router(transactions_router)

app.include_router(transfers_router)

add_pagination(app)


def main():

    print("Starting")


if __name__ == "__main__":
    main()
