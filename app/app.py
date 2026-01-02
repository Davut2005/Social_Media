from fastapi import FastAPI, HTTPException, File, UploadFile, Form, Depends
from app.schemas import CreatePost
from app.db import create_db_and_tables, Post, get_async_session
from contextlib import asynccontextmanager
#from app.images import imagekit
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
#from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
import shutil
import os
import uuid
import tempfile

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

posts = {
    1:{ "title":"1st Post", "content":"Just a 1st Post" },
    2:{ "title":"2nd Post", "content":"Just a 2nd Post" },
    3:{ "title":"3rd Post", "content":"Just a 3rd Post" },
    4:{ "title":"4th Post", "content":"Just a 4th Post" },
    5:{ "title":"5th Post", "content":"Just a 5th Post" },
}

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    caption:str = Form(""),
    session: AsyncSession = Depends(get_async_session)
):
    post = Post(
        caption = caption,
        url= "url",
        file_type= "photo",
        file_name= "name"
    )
    session.add(post)
    await session.commit()
    await session.refresh(post)
    return post

@app.get("/feed")
async def get_feed(
    session: AsyncSession = Depends(get_async_session)
):   
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [ row[0] for row in result.all() ]

    post_data = []
    for post in posts:
        post_data.append(
            {
                "id": str(post.id),
                "caption": post.caption,
                "url": post.url,
                "file_name": post.file_name,
                "file_type": post.file_type,
                "created_at": post.created_at.isoformat()
            }
        )
    return {"posts": post_data}    
