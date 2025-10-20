from sqlalchemy.orm import Session
from typing import Optional, List
from app.modules.products.models import Product
from app.modules.products.schemas import ProductCreate, ProductUpdate

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, product: ProductCreate) -> Product:
        db_product = Product(**product.model_dump())
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product
    
    def get_by_id(self, product_id: int) -> Optional[Product]:
        return self.db.query(Product).filter(Product.id == product_id).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        return self.db.query(Product).offset(skip).limit(limit).all()
    
    def get_by_category(self, category: str, skip: int = 0, limit: int = 100) -> List[Product]:
        return self.db.query(Product).filter(Product.category == category).offset(skip).limit(limit).all()
    
    def update(self, product_id: int, product_update: ProductUpdate) -> Optional[Product]:
        db_product = self.get_by_id(product_id)
        if not db_product:
            return None
        
        update_data = product_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_product, field, value)
        
        self.db.commit()
        self.db.refresh(db_product)
        return db_product
    
    def delete(self, product_id: int) -> bool:
        db_product = self.get_by_id(product_id)
        if not db_product:
            return False
        self.db.delete(db_product)
        self.db.commit()
        return True
    
    def count_total(self) -> int:
        return self.db.query(Product).count()
    
    def count_by_category(self) -> List[dict]:
        from sqlalchemy import func
        result = self.db.query(
            Product.category,
            func.count(Product.id).label('count')
        ).group_by(Product.category).all()
        return [{"category": row[0], "count": row[1]} for row in result]
