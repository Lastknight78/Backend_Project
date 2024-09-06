from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from schemas import OrderModel,TokenData, OrderModels, OrderStatus
from database import get_db
from fastapi.encoders import jsonable_encoder

import utility, auth, models, schemas

order_router = APIRouter(
    prefix='/orders',
    tags = ['orders']
)
@order_router.get('/')
async def hello():
    return {"message":"hello world"}

@order_router.post("/create-orders",status_code=status.HTTP_201_CREATED)
async def order_request(orders : schemas.OrderModel, db : Session = Depends(get_db), get_current_user : schemas.TokenData = Depends(auth.get_current_user)):
    order = schemas.OrderModels(user_id=get_current_user.id, **orders.model_dump())
    add_order = models.Order(**order.model_dump())
    db.add(add_order)
    db.commit()
    db.refresh(add_order)
    return add_order
    
@order_router.get("/total/orders")
async def order_list(db : Session = Depends(get_db), get_current_user : schemas.TokenData = Depends(auth.get_current_user)):
    user = db.query(models.User).filter(models.User.id == get_current_user.id).first()
    if user.is_staff:
        orders = db.query(models.Order).all()
        return orders
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you are not authorized as you are not a superuser")
    
@order_router.get("/total/orders/user")
async def order_by_user(db : Session = Depends(get_db), get_current_user : schemas.TokenData = Depends(auth.get_current_user)):
    user = db.query(models.User).filter(models.User.id == get_current_user.id).first()
    if user.is_staff:
        order_by_user = db.query(models.Order).filter(models.Order.user_id == get_current_user.id).all()
        if order_by_user is None:
            return {"message":"you don't have any current order"}
        return order_by_user
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you are not authorized as you are not a superuser")
        
    


@order_router.get("/one/order/{id}")
async def get_one_order(id : int, db : Session = Depends(get_db), get_current_user : schemas.TokenData = Depends(auth.get_current_user)):
    user = db.query(models.User).filter(models.User.id == get_current_user.id).first()
    if user.is_staff:
        order = db.query(models.Order).filter(models.Order.id == id).first()
        if order is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"order with id: {id} not found")
        return order
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you are not authorized as you are not a superuser")

@order_router.get("/retrieve/orders")
async def order_by_user(db : Session = Depends(get_db), get_current_user : schemas.TokenData = Depends(auth.get_current_user)):
    order_by_user = db.query(models.Order).filter(models.Order.user_id == get_current_user.id).all()
    return order_by_user
    
@order_router.get("/retrieve/specific/orders/{id}")
async def order_by_user(id : int, db : Session = Depends(get_db), get_current_user : schemas.TokenData = Depends(auth.get_current_user)):
    order_by_user = db.query(models.Order).filter(models.Order.user_id == get_current_user.id, models.Order.id == id).first()
    if order_by_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"order with id: {id} not found")
    return order_by_user
        
@order_router.put("/update/specific/order/{id}")
async def update_order(order_update : schemas.OrderModel, id : int, db : Session = Depends(get_db), get_current_user : schemas.TokenData = Depends(auth.get_current_user)):
    order_query = db.query(models.Order).filter(models.Order.id == id).first()
    if order_query is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"order with id: {id} not found")
    if order_query.user_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you are not authorized to perform this action")
    order_query.quantity = order_update.quantity
    order_query.pizza_size = order_update.pizza_size
    db.commit()
    return order_query


@order_router.patch("/order/update/staff/{id}")
async def update_order_status(OrderStatus : schemas.OrderStatus, id : int, db : Session = Depends(get_db), get_current_user : schemas.TokenData = Depends(auth.get_current_user)):
    user = db.query(models.User).filter(models.User.id == get_current_user.id).first()
    if user.is_staff:
        order = db.query(models.Order).filter(models.Order.id == id).first()
        order.order_status = OrderStatus.order_status
        db.commit()
        db.refresh(order)
        response = {
            "id": order.id,
            "quantity" : order.quantity,
            "order_status" : order.order_status,
            "pizza-size" : order.pizza_size
        }
        return response
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you are not authorized as you are not a superuser")


@order_router.delete("/delete/specific/order/{id}",status_code = status.HTTP_204_NO_CONTENT)
async def delete_order(id : int, db : Session = Depends(get_db), get_current_user : schemas.TokenData = Depends(auth.get_current_user)):
    order_query_delete = db.query(models.Order).filter(models.Order.id == id).first()
    if order_query_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"order with id: {id} not found")
    if order_query_delete.user_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you are not authorized to perform this action")
    db.delete(order_query_delete)
    db.commit()
    return order_query_delete
