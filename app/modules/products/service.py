from sqlalchemy.orm import Session
from typing import Optional, List
from app.modules.products.repository import ProductRepository
from app.modules.products.schemas import ProductCreate, ProductUpdate, ProductResponse

class ProductService:
    def __init__(self, db: Session):
        self.repository = ProductRepository(db)
        self.db = db
    
    def _create_log(self, user_id: int, action: str):
        from app.modules.logs.service import LogService
        log_service = LogService(self.db)
        log_service.create_log(user_id, action)
    
    def create_product(self, product: ProductCreate, user_id: int) -> ProductResponse:
        db_product = self.repository.create(product)
        self._create_log(user_id, f"Producto creado: {product.name} (Categoría: {product.category}, Stock: {product.stock})")
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
    
    def update_product(self, product_id: int, product_update: ProductUpdate, user_id: int) -> Optional[ProductResponse]:
        product = self.repository.get_by_id(product_id)
        if not product:
            return None
        
        updated_product = self.repository.update(product_id, product_update)
        if not updated_product:
            return None
        
        changes = []
        if product_update.name:
            changes.append(f"nombre a '{product_update.name}'")
        if product_update.category:
            changes.append(f"categoría a '{product_update.category}'")
        if product_update.price:
            changes.append(f"precio a ${product_update.price}")
        if product_update.stock is not None:
            changes.append(f"stock a {product_update.stock}")
        
        action = f"Producto actualizado (ID: {product_id}, {product.name}): cambió " + ", ".join(changes)
        self._create_log(user_id, action)
        
        return ProductResponse.model_validate(updated_product)
    
    def delete_product(self, product_id: int, user_id: int) -> bool:
        product = self.repository.get_by_id(product_id)
        if not product:
            return False
        
        deleted = self.repository.delete(product_id)
        if deleted:
            self._create_log(user_id, f"Producto eliminado: {product.name} (ID: {product_id})")
        return deleted
    
    def get_statistics(self) -> dict:
        total = self.repository.count_total()
        by_category = self.repository.count_by_category()
        return {
            "total_productos": total,
            "productos_por_categoria": by_category
        }
