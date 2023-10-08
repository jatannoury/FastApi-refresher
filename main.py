from fastapi import Body,FastAPI

app = FastAPI()

BOOKS = [
    {"Title":"Joseph1","Author":"Joseph1","Category":"science"},
    {"Title":"Joseph2","Author":"Joseph2","Category":"science"},
    {"Title":"Joseph3","Author":"Joseph3","Category":"math"},
    {"Title":"Joseph4","Author":"Joseph4","Category":"math"},
    {"Title":"Joseph5","Author":"Joseph5","Category":"physics"},
    {"Title":"Joseph2","Author":"Joseph6","Category":"physics"},
]

@app.get("/books")
async def read_all_books():
    return BOOKS

#Path Parameters
"""
Always note that order matters for path parameters. So considering the following:

@app.get("/books/{book_id}")
async def read_all_books():
    ...
@app.get("/books/mybook")
async def read_all_books():
    ...

the first funciton will always be called when querying 127.0.0.1:8000/books/mybook
"""
@app.get("/books/{book_title}") #Note that the path param name specified in the app.get should be used as is as the function param
async def read_all_books(book_title: str):
    return list(filter(lambda element:element['Title'].casefold() == book_title.casefold(),BOOKS))



#ALERT: THIS WILL NEVER BE CALLED BECAUSE OF THE FUNCTION ABOVE
@app.get("/books/mybook")
async def read_all_books():
    return {"Title":"Joseph1","Author":"Joseph1","Category:":"Joseph6"}


#QUERY PARAMETERS
# @app.get('/books/')
# async def read_category_by_query(category: str):
#     return list(filter(lambda element:element['Category'].casefold() == category.casefold(),BOOKS))

@app.get('/books/{book_author}')
async def read_author_category_by_query(book_author: str,category: str):
    print(category)
    print(category)
    return list(filter(lambda element:element['Author'].casefold() == book_author.casefold() and element['Category'].casefold() == category.casefold(),BOOKS))

@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)
