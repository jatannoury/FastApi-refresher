from typing import Optional

from fastapi import FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel,Field
from starlette import status
app = FastAPI()


class Book:
    id:int
    title:str
    author:str
    description:str
    rating:int

    def __init__(self,id,title,author,description,rating):
        self.id = id
        self.title = title
        self.author=author
        self.description=description
        self.rating=rating

class BookRequest(BaseModel):
    id: Optional[int] = Field(title="ID is not needed")
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1,max_length=100)
    rating: int = Field(gt=-1,lt=6)

    class Config:
        json_schema_extra = {
            'example':{
                "title":"A new book",
                'author':"Joseph",
                "description":"Description of a new book",
                "rating":5
            }
        }

BOOKS = [
    Book(1,'Computer Science Pro','joseph','A very nice book!',5),
    Book(2,'Be Fast with FastApi','joseph','A very great book!',5),
    Book(3,'Master Endpoints','joseph','An awesom book!',5),
]
@app.get("/books",status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}",status_code=status.HTTP_200_OK)
async def read_book(book_id:int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    return HTTPException(status_code=404,detail=f"The book with id {book_id} is not found")

@app.get("/books/",status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating:int = Query(gt=-1,lt=6)):
    return list(filter(lambda book:book.rating == book_rating,BOOKS))

@app.post("/create-book",status_code=status.HTTP_201_CREATED)
async def create_book(book_request:BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


@app.put("/books/update_book",status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book:BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404,detail="item not found")


@app.delete("/books/{book_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break
    if not book_changed:
        raise HTTPException(status_code=404,detail="item not found")

def find_book_id(book:Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book