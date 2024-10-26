import asyncio
from backend.src.products.dao import ProductDAO
from backend.src.orders.dao import OrderDAO

async def main():
    orders= await OrderDAO.count()
    print(orders)

asyncio.run(main())