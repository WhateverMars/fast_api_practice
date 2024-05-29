from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    text: str
    is_done: bool = False


items = []


@app.get("/")
def root():
    return {"Hello": "World"}


@app.post("/items")
def create_item(item: Item):
    items.append(item)
    return items


@app.get("/items")
def list_items(limit: int = 10):
    return items[0:limit]


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int) -> Item:
    try:
        return items[item_id]
    except IndexError:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found.")


@app.patch("/items/{item_id}/is_done", response_model=Item)
def mark_item_as_done(item_id: int):
    try:
        items[item_id].is_done = True
        return items[item_id]
    except IndexError:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found.")


@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    try:
        items[item_id] = item
        return items[item_id]
    except IndexError:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found.")


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    try:
        items.pop(item_id)
        return {"message": f"Item {item_id} has been deleted."}
    except IndexError:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found.")
