import asyncio
from backend.products.dao import ProductDAO

async def main():
    product = await ProductDAO.find_by_id(model_id=1)
    print(product)

asyncio.run(main())