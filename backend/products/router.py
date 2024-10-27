from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db

from backend.products.dao import ProductDAO
from backend.products.schemas import (
    FullProductResponse,
    CreateProduct,
    UpdateProduct,
)

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=FullProductResponse, status_code=201)
async def create_product(
    product: CreateProduct, session: AsyncSession = Depends(get_db)
):
    return await ProductDAO.create(session, product)


@router.post(
    "/many/", response_model=list[FullProductResponse], status_code=201
)
async def create_product_many(
    product: list[CreateProduct], session: AsyncSession = Depends(get_db)
):
    return await ProductDAO.create_many(session, product)


@router.get("/")
async def product_list(session: AsyncSession = Depends(get_db)):
    return await ProductDAO.find_all(session)


@router.get("/{product_id}", response_model=FullProductResponse)
async def get_product(
    product_id: int, session: AsyncSession = Depends(get_db)
):
    return await ProductDAO.find_by_id(session, product_id)


@router.put(
    "/{product_id}", response_model=FullProductResponse, status_code=200
)
async def update_product(
    product_id: int,
    updated_data: UpdateProduct,
    session: AsyncSession = Depends(get_db),
):
    return await ProductDAO.update(
        session, product_id, updated_data, partial=False
    )


@router.patch(
    "/{product_id}", response_model=FullProductResponse, status_code=200
)
async def partial_update_product(
    product_id: int,
    updated_data: UpdateProduct,
    session: AsyncSession = Depends(get_db),
):
    return await ProductDAO.update(
        session, product_id, updated_data, partial=True
    )


@router.delete("/{product_id}", status_code=200)
async def delete_product(
    product_id: int, session: AsyncSession = Depends(get_db)
):
    return await ProductDAO.destroy(session, product_id)
