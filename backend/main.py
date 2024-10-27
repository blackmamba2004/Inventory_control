from fastapi import FastAPI

from backend.orders.router import router as order_router
from backend.products.router import router as product_router

app = FastAPI()

app.include_router(product_router)
app.include_router(order_router)


@app.get("/")
async def root():
    return {"message": "Hello, world!"}
