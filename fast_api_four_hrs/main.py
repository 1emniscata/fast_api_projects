from typing import Optional

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# ?limit=10&published=true
@app.get("/blog")
def index(limit=10, published: bool = True, sort: Optional[str] = None):
    # return published
    if published:
        return {"data": f"{limit} published blogs from the db"}
    else:
        return {"data": f"{limit} blogs from the db"}


@app.get("/blog/unpublished")
def unpublished():
    return {"data": "all unpublished blogs"}


@app.get("/blog/{blog_id}")
def show(blog_id: int):
    return {"data": blog_id}


@app.get("/blog/{blog_id}/comments")
def comments(blog_id, limit=10):
    return {"data": {"1", "2"}}


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.post("/blog")
def create_blog(blog: Blog):
    return {"data": f"Blog is created with title as {blog.title}"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9000)
