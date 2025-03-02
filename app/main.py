"""
Library API

Author: Sandeep Sharma
Author Email: sandeeptech8@gmail.com
"""

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from app.api.books import router as books_router
from app.core import exceptions as custom_exceptions
from app.core import exception_handlers

app = FastAPI()

# Register routers
app.include_router(books_router, prefix='/books', tags=['Books'])

# Register exception handlers
app.add_exception_handler(RequestValidationError,
                          exception_handlers.validation_exception_handler)
app.add_exception_handler(custom_exceptions.DuplicateEntryException,
                          exception_handlers.duplicate_entry_exception_handler)
app.add_exception_handler(custom_exceptions.ForeignKeyNotFoundException,
                          exception_handlers.foreign_key_not_found_exception_handler)
app.add_exception_handler(
    Exception, exception_handlers.global_exception_handler)
