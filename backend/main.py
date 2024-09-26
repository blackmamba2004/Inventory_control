from fastapi import FastAPI
from settings.database import engine

from src.routes.orders import models as order_models
from src.routes.products import models as product_models

from src.routes.products.main import router as product_router
from src.routes.orders.main import router as order_router


order_models.Base.metadata.create_all(bind=engine)
product_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(product_router)
app.include_router(order_router)

@app.get('/')
async def root():
    return {'message': 'Hello, world!'}