from email.policy import default

from sympy import limit

from fastapi import FastAPI,HTTPException,Query
from app.services.products import get_all_products 

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI E-commerce application!"}
 
@app.get("/products")
def list_products(
    name: str = Query(default=None, max_length=50,min_length=1 ,description="Search by product name"),
    sort_by_price: bool = Query(default=False, description="Sort products by price"),
    order: str = Query(default="asc",  description="Sort order when sort_by_price is true. Allowed values: 'asc' or 'desc'"),
    limit: int = Query(default=10, ge=1, le=100, description="Number of items to return"),
    offset: int = Query(default=0, ge=0, description="Pagination offset")
):
    products = get_all_products()
    if name:
        needle = name.strip().lower()
        products = [p for p in products if needle in p.get("name", "").lower()]

        if not products:
            raise HTTPException(status_code=404, detail=f"No product found matching the name={name}")

    if sort_by_price:
        reverse = order == 'desc'
        products = sorted(products,key=lambda p:p.get("price",0),reverse=reverse)

    total = len(products)
    products = products[offset:offset+limit]
    return {
        "total": total,
        "limit": limit,
        "items": products
    }

