from sqlmodel import create_engine, Session

DATABASE_URL = "sqlite:///bank.db"

# echo True helps to log database info in the terminal
engine = create_engine(DATABASE_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session
