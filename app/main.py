"""
Library API

Author: Sandeep Sharma
Author Email: sandeeptech8@gmail.com
"""

from fastapi import FastAPI
from app.api.books import router as books_router

app = FastAPI()

# Register routers
app.include_router(books_router, prefix='/books', tags=['Books'])
