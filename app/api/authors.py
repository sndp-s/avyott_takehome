"""
Authors endpoints.
"""

from typing import Annotated
from fastapi import APIRouter, Depends, Query, Path
from app.db.connection import get_db
from app.services import authors as authors_service
from app.models import authors as authors_models
from app.models.responses import APIResponse

router = APIRouter()


# NOTE :: GOOD TO HAVE: Accept a parameter to return all the books associated with each author.
@router.get("")
async def get_all_authors(
    db=Depends(get_db),
    offset: Annotated[int, Query(ge=0, description="Starting index")] = 0,
    limit: Annotated[int, Query(
        ge=1, le=100, description="Number of items to retrieve")] = 10
) -> APIResponse[list[authors_models.Author]]:
    """Returns all the authors in the library."""
    all_authors = authors_service.get_all_authors_service(db, offset, limit)
    return APIResponse(
        data=all_authors,
        message="Authors fetched successfully"
    )


# NOTE :: GOOD TO HAVE: Accept a parameter to return all the books associated with the author.
@router.get("/{author_id}")
async def get_author(
    author_id: Annotated[int, Path()],
    db=Depends(get_db)
) -> APIResponse[authors_models.Author]:
    """
    Returns the Author corresponding to the given author_id.
    """
    author = authors_service.get_author_service(db, author_id)
    return APIResponse(
        data=author,
        message='Author fetched successfully'
    )


@router.post("")
async def create_author(
    author: authors_models.AuthorCreate,
    db=Depends(get_db)
) -> APIResponse[authors_models.Author]:
    """
    Adds a new Author to the library.
    """
    added_author = authors_service.add_new_author_service(db, author)
    return APIResponse(
        data=added_author,
        message="Author added successfully"
    )


@router.put("/{author_id}")
async def update_author(
    author_id: Annotated[int, Path()],
    author: authors_models.AuthorUpdate,
    db=Depends(get_db)
) -> APIResponse[authors_models.Author]:
    """
    Update an existing Author.
    """
    updated_author = authors_service.update_author_service(db, author_id, author.model_dump(exclude_unset=True))

    return APIResponse(
        data=updated_author,
        message="Author updated successfully."
    )
