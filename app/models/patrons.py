"""
Patrons model
"""

from datetime import date
from pydantic import BaseModel, EmailStr

class PatronBase(BaseModel):
    """
    Base class for Patron entity.
    """
    first_name: str
    last_name: str
    email: EmailStr


class Patron(BaseModel):
    """
    Patron model.
    """
    id: int
    registration_date: date


class PatronCreate(PatronBase):
    """
    Model for 'Create patron' API request body.
    """
    pass


class PatronUpdate(PatronBase):
    """
    Model for 'Update patron' API request body.
    """
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
