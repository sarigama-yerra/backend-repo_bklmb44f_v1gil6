"""
Database Schemas for Northmann Group site

Each Pydantic model maps to a MongoDB collection using the lowercase
of the class name as the collection name.
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class Lead(BaseModel):
    """
    Website contact leads
    Collection name: "lead"
    """
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    company: Optional[str] = Field(None, description="Company name")
    phone: Optional[str] = Field(None, description="Phone number")
    message: str = Field(..., description="Inquiry details")
    source: Optional[str] = Field("website", description="Lead source")


class Newsletter(BaseModel):
    """
    Newsletter subscribers
    Collection name: "newsletter"
    """
    email: EmailStr = Field(..., description="Subscriber email")
    name: Optional[str] = Field(None, description="Subscriber name")


class Testimonial(BaseModel):
    """
    Client testimonials (optional content collection)
    Collection name: "testimonial"
    """
    author: str = Field(..., description="Client name")
    role: Optional[str] = Field(None, description="Client role or company")
    quote: str = Field(..., description="Testimonial text")
