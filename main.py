from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import Session
from tables import Post
from datetime import date
from typing import Optional

app = FastAPI()

class Item(BaseModel):
    author: str
    title: str
    content: str

class EditItem(BaseModel):
    pass
# REPLACE WITH YOUR ACTUAL USER, SERVER AND DB INFO
engine = create_engine('HERE')

@app.post("/posts")
async def create_post(item: Item):
    with Session(engine) as session:
        post = Post(
            author = item.author,
            title = item.title,
            content = item.content,
            date_posted = date.today()
        )

        session.add(post)
        session.commit()
    
@app.delete("/posts/{id}")
async def delete_post(id:int):
    with Session(engine) as session:
        if not session.query(Post).filter(Post.post_id==id).first():
            raise HTTPException(status_code=404, detail="Post not found")
        
        session.query(Post).filter(Post.post_id==id).delete()
        session.commit()
            
@app.get("/posts")
async def show_posts(skip: int = 0, limit: int = 10):
    with Session(engine) as session:
        stmt = select(Post).order_by(Post.post_id.desc()).limit(limit)
        posts = session.execute(stmt)

        data: list[Post] = []
        for post in posts.scalars():
            data.append(post)

        return data
    
@app.put("/edit_post")
async def edit_post(data: dict):
    with Session(engine) as session:
        post = session.get(Post, data["id"])
        setattr(post, data["attribute"], data["edit"])
        session.commit()