from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

class Base(DeclarativeBase):
    pass

url =  "mysql+pymysql://root:new_password@localhost:3309/pizza_delivery?charset=utf8mb4"
engine = create_engine(url=url)

sessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

def get_db():
    try:
        session = sessionLocal()
        yield session
    finally:
        session.close()
