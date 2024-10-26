from fastapi import FastAPI

from backend.src.orders import models as order_models
from backend.src.products import models as product_models

from backend.src.products.router import router as product_router
from backend.src.orders.router import router as order_router

app = FastAPI()

app.include_router(product_router)
app.include_router(order_router)

@app.get('/')
async def root():
    return {'message': 'Hello, world!'}