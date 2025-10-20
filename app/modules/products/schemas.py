from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from decimal import Decimal

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    category: str = Field(..., min_length=1, max_length=100)
    price: Decimal = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    
    @field_validator('price')
    @classmethod
    def validate_price(cls, v):
        if v <= 0:
            raise ValueError('El precio debe ser mayor que 0')
        return round(v, 2)

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[Decimal] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    
    @field_validator('price')
    @classmethod
    def validate_price(cls, v):
        if v is not None:
            if v <= 0:
                raise ValueError('El precio debe ser mayor que 0')
            return round(v, 2)
        return v

class ProductResponse(ProductBase):
    id: int
    created: datetime
    updated: Optional[datetime] = None
    
    class Config:
        from_attributes = True
