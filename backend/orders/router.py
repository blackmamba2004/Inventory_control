from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db

from backend.orders.dao import OrderDAO
from backend.orders.schemas import (
    FullOrderResponse,
    Order,
    ProductItem,
    UpdateOrderState,
)

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", response_model=FullOrderResponse)
async def create_order(
    data: list[ProductItem], session: AsyncSession = Depends(get_db)
):
    return await OrderDAO.create(session, data)


@router.get("/", response_model=list[Order])
async def order_list(session: AsyncSession = Depends(get_db)):
    return await OrderDAO.find_all(session)


@router.get("/{order_id}", response_model=FullOrderResponse)
async def get_order(order_id: int, session: AsyncSession = Depends(get_db)):

    return await OrderDAO.find_full_order(session, order_id=order_id)


@router.patch("/{order_id}/status", response_model=Order)
async def update_order_status(
    order_id: int,
    updated_data: UpdateOrderState,
    session: AsyncSession = Depends(get_db),
):

    order = await OrderDAO.update(
        session, order_id, updated_data, partial=True
    )

    return order
