# Web Services Assignment
# Student: B00157067
# Reads products.csv, converts to JSON and loads into MongoDB

import csv
import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="../.env")

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
collection = db["products"]

# Read CSV and convert to list of dicts
with open("products.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    products = []
    for row in reader:
        products.append({
            "ProductID": int(row["ProductID"]),
            "Name": row["Name"],
            "UnitPrice": float(row["UnitPrice"]),
            "StockQuantity": int(row["StockQuantity"]),
            "Description": row["Description"]
        })

# Save as JSON file
with open("products.json", "w") as f:
    json.dump(products, f, indent=2)

# Insert into MongoDB
collection.drop()
collection.insert_many(products)

print(f"Loaded {len(products)} products into MongoDB.")