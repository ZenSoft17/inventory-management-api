from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.utils import success_response, error_response
from app.modules.products.service import ProductService
from app.modules.products.schemas import ProductCreate, ProductUpdate, ProductResponse
from app.modules.users.controller import get_current_user
from app.modules.users.schemas import UserResponse

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    try:
        service = ProductService(db)
        new_product = service.create_product(product)
        return success_response(new_product.model_dump(), "Producto creado correctamente")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/", response_model=dict)
def get_all_products(
    skip: int = 0,
    limit: int = 100,
    category: str = None,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    try:
        service = ProductService(db)
        if category:
            products = service.get_products_by_category(category, skip, limit)
        else:
            products = service.get_all_products(skip, limit)
        return success_response([product.model_dump() for product in products], "Productos obtenidos correctamente")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/statistics", response_model=dict)
def get_statistics(
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    try:
        service = ProductService(db)
        stats = service.get_statistics()
        return success_response(stats, "Estadísticas obtenidas correctamente")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/{product_id}", response_model=dict)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    service = ProductService(db)
    product = service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return success_response(product.model_dump(), "Productos obtenidos correctamente")

@router.put("/{product_id}", response_model=dict)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    try:
        service = ProductService(db)
        updated_product = service.update_product(product_id, product_update)
        if not updated_product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
        return success_response(updated_product.model_dump(), "Producto actualizado correctamente")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.delete("/{product_id}", response_model=dict)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    service = ProductService(db)
    deleted = service.delete_product(product_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return success_response(None, "Producto eliminado correctamente")
