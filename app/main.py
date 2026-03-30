# Web Services Assignment - FastAPI Application
# Student: B00157067

import os
import requests
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from dotenv import load_dotenv
from prometheus_fastapi_instrumentator import Instrumentator

# Load environment variables and connect to MongoDB
load_dotenv(dotenv_path="../.env")

app = FastAPI()
Instrumentator().instrument(app).expose(app)

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
collection = db["products"]


# Pydantic model for product validation
class Product(BaseModel):
    ProductID: int
    Name: str
    UnitPrice: float
    StockQuantity: int
    Description: str


# Convert MongoDB ObjectId to string
def fix_id(doc):
    doc["_id"] = str(doc["_id"])
    return doc


# Get a single product by ProductID
@app.get("/getSingleProduct/{product_id}")
def get_single_product(product_id: int):
    product = collection.find_one({"ProductID": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return fix_id(product)


# Get all products
@app.get("/getAll")
def get_all():
    products = list(collection.find())
    return [fix_id(p) for p in products]


# Add a new product
@app.post("/addNew")
def add_new(product: Product):
    existing = collection.find_one({"ProductID": product.ProductID})
    if existing:
        raise HTTPException(status_code=400, detail="ProductID already exists")
    collection.insert_one(product.dict())
    return {"message": "Product added successfully"}


# Delete a product by ProductID
@app.delete("/deleteOne/{product_id}")
def delete_one(product_id: int):
    result = collection.delete_one({"ProductID": product_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}


# Get products where name starts with a given letter
@app.get("/startsWith/{letter}")
def starts_with(letter: str):
    if len(letter) != 1:
        raise HTTPException(status_code=400, detail="Please provide a single letter")
    products = list(collection.find({"Name": {"$regex": f"^{letter}", "$options": "i"}}))
    return [fix_id(p) for p in products]


# Get products from start ID to end ID in batches of 10
@app.get("/paginate")
def paginate(start_id: int, end_id: int):
    products = list(collection.find(
        {"ProductID": {"$gte": start_id, "$lte": end_id}}
    ).limit(10))
    if not products:
        raise HTTPException(status_code=404, detail="No products found in that range")
    return {
        "start_id": start_id,
        "end_id": end_id,
        "results": [fix_id(p) for p in products]
    }


# Convert product price from USD to EUR using live exchange rate
@app.get("/convert/{product_id}")
def convert(product_id: int):
    product = collection.find_one({"ProductID": product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
    rate = response.json()["rates"]["EUR"]
    eur_price = round(product["UnitPrice"] * rate, 2)
    return {
        "Name": product["Name"],
        "UnitPrice_USD": product["UnitPrice"],
        "UnitPrice_EUR": eur_price,
        "ExchangeRate": rate
    }