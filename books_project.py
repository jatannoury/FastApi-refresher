from typing import Optional

from fastapi import FastAPI, Body
from pydantic import BaseModel,Field
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
@app.get("/books")
async def read_all_books():
    return BOOKS

@app.get("/books/{book_id}")
async def read_book(book_id:int):
    for book in BOOKS:
        if book.id == book_id:
            return book

@app.post("/create-book")
async def create_book(book_request:BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))



def find_book_id(book:Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book