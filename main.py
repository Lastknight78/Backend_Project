from fastapi import FastAPI
from order_route import order_router
from auth_route import auth_router
from database import engine,Base
from models import User, Order
app = FastAPI()

app.include_router(auth_router)
app.include_router(order_router)

Base.metadata.create_all(bind=engine)
