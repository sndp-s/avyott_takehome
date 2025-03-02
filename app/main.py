"""
Library API

Author: Sandeep Sharma
Author Email: sandeeptech8@gmail.com
"""

from fastapi import FastAPI
from app.api.books import router as books_router
from app.core import exception_handlers

app = FastAPI()

# Register routers
app.include_router(books_router, prefix='/books', tags=['Books'])

# Register exception handlers
app.add_exception_handler(Exception, exception_handlers.global_exception_handler)
