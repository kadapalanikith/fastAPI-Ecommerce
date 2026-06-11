from fastapi import FastAPI
from app.services.products import get_all_products 

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI E-commerce application!"}

@app.get("/products")
def get_products():
    return get_all_products()

