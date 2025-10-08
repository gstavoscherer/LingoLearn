from typing import Generic, TypeVar, Any, Optional, List
from sqlalchemy import select, update, delete
from sqlalchemy.orm import Session, joinedload

ModelType = TypeVar('ModelType')

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: type[ModelType], db: Session):
        self.model = model
        self.db = db

    def get(self, id: int, load_relationships: Optional[List[str]] = None) -> Optional[ModelType]:
        stmt = select(self.model).where(self.model.id == id)
        if load_relationships:
            for rel in load_relationships:
                stmt = stmt.options(joinedload(getattr(self.model, rel)))
        return self.db.scalars(stmt).first()

    def get_by(self, **filters: Any) -> Optional[ModelType]:
        stmt = select(self.model).filter_by(**filters)
        return self.db.scalars(stmt).first()

    def list_all(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[dict] = None,
        order_by: Optional[str] = None
    ) -> List[ModelType]:
        stmt = select(self.model).offset(skip).limit(limit)
        if filters:
            stmt = stmt.filter_by(**filters)
        if order_by:
            stmt = stmt.order_by(order_by)
        return list(self.db.scalars(stmt).all())

    def create(self, **data: Any) -> ModelType:
        obj = self.model(**data)
        self.db.add(obj)
        return obj

    def update(self, obj: ModelType, **data: Any) -> ModelType:
        for key, value in data.items():
            setattr(obj, key, value)
        return obj

    def delete(self, obj: ModelType) -> None:
        self.db.delete(obj)

    def bulk_update(self, ids: List[int], **data: Any) -> None:
        stmt = update(self.model).where(self.model.id.in_(ids)).values(**data)
        self.db.execute(stmt)

    def bulk_delete(self, ids: List[int]) -> None:
        stmt = delete(self.model).where(self.model.id.in_(ids))
        self.db.execute(stmt)