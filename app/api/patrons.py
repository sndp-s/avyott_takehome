"""
Patrons endpoints.
"""

from typing import Annotated
from fastapi import APIRouter, Depends, Query, Path
from app.db.connection import get_db
from app.services import patrons as patrons_service
from app.models import patrons as patrons_models
from app.models.responses import APIResponse

router = APIRouter()


@router.get("")
async def get_all_patrons(
    db=Depends(get_db),
    offset: Annotated[int, Query(ge=0, description="Starting index")] = 0,
    limit: Annotated[int, Query(
        ge=1, le=100, description="Number of items to retrieve")] = 10
) -> APIResponse[list[patrons_models.Patron]]:
    """Returns all the Patrons associated with the library."""
    all_patrons = patrons_service.get_all_patrons_service(db, offset, limit)
    return APIResponse(
        data=all_patrons,
        message="patrons fetched successfully"
    )


@router.get("/{patron_id}")
async def get_patron(
    patron_id: Annotated[int, Path()],
    db=Depends(get_db)
) -> APIResponse[patrons_models.Patron]:
    """
    Returns the patron corresponding to the given patron_id.
    """
    patron = patrons_service.get_patron_service(db, patron_id)
    return APIResponse(
        data=patron,
        message='patrons fetched successfully'
    )


@router.post("")
async def create_patron(
    patron: patrons_models.PatronCreate,
    db=Depends(get_db)
) -> APIResponse[patrons_models.Patron]:
    """
    Adds a new Patron to the library.
    """
    added_patron = patrons_service.add_new_patron_service(db, patron)
    return APIResponse(
        data=added_patron,
        message="Patron added successfully"
    )
