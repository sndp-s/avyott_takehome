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
from app.core.APIKeyAuthMiddleware import APIKeyAuthMiddleware

app = FastAPI()

# Customise openapi to requrie a x-api-header header field for all endpoints.
app.original_openapi = app.openapi
def custom_openapi():
    """
    Adds a required fields to input x-api-key header in every APIs. 
    """
    if app.openapi_schema:
        return app.openapi_schema

    # Call the original openapi function to generate the schema
    openapi_schema = app.original_openapi()
    # Add a global header parameter to every operation
    header_param = {
        "in": "header",
        "name": "x-api-key",
        "description": "API Key required for authentication",
        "required": True,
        "schema": {"type": "string"}
    }
    for path in openapi_schema.get("paths", {}).values():
        for operation in path.values():
            parameters = operation.get("parameters", [])
            parameters.append(header_param)
            operation["parameters"] = parameters
    app.openapi_schema = openapi_schema
    return openapi_schema
app.openapi = custom_openapi

# Register middlewares
app.add_middleware(APIKeyAuthMiddleware)

# Register routers
app.include_router(books_router, prefix='/books', tags=['Books'])

# Register exception handlers
app.add_exception_handler(RequestValidationError,
                          exception_handlers.validation_exception_handler)
app.add_exception_handler(custom_exceptions.DuplicateEntryException,
                          exception_handlers.duplicate_entry_exception_handler)
app.add_exception_handler(custom_exceptions.ForeignKeyNotFoundException,
                          exception_handlers.foreign_key_not_found_exception_handler)
app.add_exception_handler(custom_exceptions.DatabaseOperationException,
                          exception_handlers.database_operation_exception_handler)
app.add_exception_handler(custom_exceptions.LoanPendingException,
                          exception_handlers.loan_pending_exception_handler)
app.add_exception_handler(
    Exception, exception_handlers.global_exception_handler)
