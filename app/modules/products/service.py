from sqlalchemy.orm import Session
from typing import Optional, List
from app.modules.products.repository import ProductRepository
from app.modules.products.schemas import ProductCreate, ProductUpdate, ProductResponse

class ProductService:
    def __init__(self, db: Session):
        self.repository = ProductRepository(db)
    
    def create_product(self, product: ProductCreate) -> ProductResponse:
        db_product = self.repository.create(product)
        return ProductResponse.model_validate(db_product)
    
    def get_product_by_id(self, product_id: int) -> Optional[ProductResponse]:
        product = self.repository.get_by_id(product_id)
        if not product:
            return None
        return ProductResponse.model_validate(product)
    
    def get_all_products(self, skip: int = 0, limit: int = 100) -> List[ProductResponse]:
        products = self.repository.get_all(skip, limit)
        return [ProductResponse.model_validate(product) for product in products]
    
    def get_products_by_category(self, category: str, skip: int = 0, limit: int = 100) -> List[ProductResponse]:
        products = self.repository.get_by_category(category, skip, limit)
        return [ProductResponse.model_validate(product) for product in products]
    
    def update_product(self, product_id: int, product_update: ProductUpdate) -> Optional[ProductResponse]:
        updated_product = self.repository.update(product_id, product_update)
        if not updated_product:
            return None
        return ProductResponse.model_validate(updated_product)
    
    def delete_product(self, product_id: int) -> bool:
        return self.repository.delete(product_id)
    
    def get_statistics(self) -> dict:
        total = self.repository.count_total()
        by_category = self.repository.count_by_category()
        return {
            "total_products": total,
            "products_by_category": by_category
        }
