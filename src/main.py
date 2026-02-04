"""
API Service - Sample REST API
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="API Service", version="1.0.0")


class HealthResponse(BaseModel):
    status: str
    timestamp: str


class Item(BaseModel):
    id: int
    name: str
    description: str = None


# In-memory storage
items_db = {}


@app.get("/")
def root():
    return {"message": "Welcome to API Service", "version": "1.0.0"}


@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat()
    )


@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]


@app.post("/items")
def create_item(item: Item):
    items_db[item.id] = item
    return item


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
