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
