from sqlmodel import create_engine, SQLModel, Session

engine = create_engine("sqlite:///route_board.db") # conecta ao banco local "dispatch.db"

def create_db():  # L~e os modelos do model com o parametro (table=True)
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session