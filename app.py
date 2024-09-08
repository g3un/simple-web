from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional

app = FastAPI()


class Memo(BaseModel):
    title: str
    content: str


db: Dict[int, Memo] = {}
next_id = 1


@app.get("/memos")
def get_memos():
    return db


@app.get("/memos/{id}")
def get_memo(id: int):
    if id not in db:
        raise HTTPException(status_code=404, detail="Memo not found")
    return db[id]


@app.post("/memos")
def post_memo(memo: Memo):
    global next_id
    db[next_id] = memo
    next_id += 1
    return {"id": next_id - 1}


@app.delete("/memos/{id}")
def delete_memo(id: int):
    if id not in db:
        raise HTTPException(status_code=404, detail="Memo not found")
    del db[id]
    return {"detail": "Memo deleted"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", reload=True)
