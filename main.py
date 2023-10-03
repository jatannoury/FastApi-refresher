from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {"Title":"Joseph1","Author":"Joseph1","Category:":"Joseph6"},
    {"Title":"Joseph2","Author":"Joseph2","Category:":"Joseph5"},
    {"Title":"Joseph3","Author":"Joseph3","Category:":"Joseph4"},
    {"Title":"Joseph4","Author":"Joseph4","Category:":"Joseph3"},
    {"Title":"Joseph5","Author":"Joseph5","Category:":"Joseph2"},
    {"Title":"Joseph6","Author":"Joseph6","Category:":"Joseph1"},
]

@app.get("/books")
async def read_all_books():
    return BOOKS