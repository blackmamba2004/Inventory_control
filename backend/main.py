from fastapi import FastAPI

from src.orders import models as order_models
from src.products import models as product_models

from src.products.main import router as product_router
from src.orders.main import router as order_router

app = FastAPI()

app.include_router(product_router)
app.include_router(order_router)

@app.get('/')
async def root():
    return {'message': 'Hello, world!'}