from fastapi import FastAPI
from sqlmodel import SQLModel
from app.database import engine

from app.routes.clients import router as clients_router
from app.routes.transactions import router as transactions_router


app = FastAPI()
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)
app.include_router(clients_router)
app.include_router(transactions_router)

def main():

    print("Starting")


if __name__ == '__main__':
    main()


