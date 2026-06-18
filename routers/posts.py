from fastapi import APIRouter
from crud.posts_crud import create_post, delete_post, show_posts, edit_post, Item
from database import get_session

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

@router.post("/create-post")
async def r_create_post(item: Item):
    with get_session() as session:
        create_post(item, session)
    
@router.delete("/delete-post/")
async def r_delete_post(id: int):
    with get_session() as session:
        delete_post(id, session)
            
@router.get("")
async def r_show_posts(limit: int = 10):
    with get_session() as session:
        posts = show_posts(session, limit)

    return posts
    
@router.put("/edit-post")
async def r_edit_post(data: dict):
    with get_session() as session:
        edit_post(data, session)