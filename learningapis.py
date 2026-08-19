from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Simple Item API")

# Fake in-memory database for learnign purposes
db = [
    {"id": 1, "name": "Laptop", "price": 9500.00},
    {"id": 2, "name": "Mouse", "price": 250.00},
    {"id": 3, "name": "Monitor", "price": 2500.00},
    {"id": 4, "name": "Keyboard", "price": 450.00},
    {"id": 5, "name": "headphones", "price": 650.00}
]

# Pydantic schema for request validation
class Item(BaseModel):
    name: str
    price: float

# ------------------------------------------
# Implementing APIs
# ------------------------------------------

# Get: Fetch all items
@app.get("/items", response_model=List[dict])
def get_items():
    return db

#Get: Fetch a single item by ID
@app.get("/items/{item_id}")
def get_item(item_id: int):
    for item in db:
        if item["id"] == item_id:
            return item
        raise HTTPException(status_code=404, detail="Item not Found")

# POST: Create a new item
@app.post("/items, status_code=201")
def create_item(item: Item):
    new_id = max([i["id"] for i in db], default=0) +1
    new_item = {"id": new_id, **item.model_dump()}
    db.append(new_item)
    return new_item

# PUT: Update an existing item
@app.put("/items/{item_id}")
def update_item(item_id: int, updated_item: Item):
    for index, item in enumerate(db):
        if item["id"] == item_id:
            db[index] = {"id": item_id, **updated_item.model_dump()}
            return db[index]
    raise HTTPException(status_code=404, detail="Item not found")

# DELETE: Remove an item
@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    for index, item in enumerate(db):
        if item["id"] == item_id:
            db.pop(index)
            return
    raise HTTPException(status_code=404, detail="Item not found")
