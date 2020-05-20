from typing import Any, List, Generator

from fastapi import Depends, FastAPI, HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND

from . import actions, models, schemas
from .db import SessionLocal, engine

# Create all tables in database.
# Comment this out if you using migrations.
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency to get DB session.
def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def index() -> Any:
    return {"message": "Hello world!"}


@app.get("/posts", response_model=List[schemas.Post], tags=["posts"])
def list_posts(db: Session = Depends(get_db), skip: int = 0, limit: int = 100) -> Any:
    posts = actions.post.get_all(db=db, skip=skip, limit=limit)
    return posts


@app.post(
    "/posts", response_model=schemas.Post, status_code=HTTP_201_CREATED, tags=["posts"]
)
def create_post(*, db: Session = Depends(get_db), post_in: schemas.PostCreate) -> Any:
    post = actions.post.create(db=db, obj_in=post_in)
    return post


@app.put(
    "/posts/{id}",
    response_model=schemas.Post,
    responses={HTTP_404_NOT_FOUND: {"model": schemas.HTTPError}},
    tags=["posts"],
)
def update_post(
    *, db: Session = Depends(get_db), id: UUID4, post_in: schemas.PostUpdate,
) -> Any:
    post = actions.post.get(db=db, id=id)
    if not post:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Post not found")
    post = actions.post.update(db=db, db_obj=post, obj_in=post_in)
    return post


@app.get(
    "/posts/{id}",
    response_model=schemas.Post,
    responses={HTTP_404_NOT_FOUND: {"model": schemas.HTTPError}},
    tags=["posts"],
)
def get_post(*, db: Session = Depends(get_db), id: UUID4) -> Any:
    post = actions.post.get(db=db, id=id)
    if not post:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Post not found")
    return post


@app.delete(
    "/posts/{id}",
    response_model=schemas.Post,
    responses={HTTP_404_NOT_FOUND: {"model": schemas.HTTPError}},
    tags=["posts"],
)
def delete_post(*, db: Session = Depends(get_db), id: UUID4) -> Any:
    post = actions.post.get(db=db, id=id)
    if not post:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Post not found")
    post = actions.post.remove(db=db, id=id)
    return post
