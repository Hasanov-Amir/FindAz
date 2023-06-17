import uuid

from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from sqlalchemy.sql import func

from core.extensions import db


Column = db.Column


class CRUDMixin:
    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()
    
    @classmethod
    def get(cls, id):
        return cls.query.get(id)
    
    @classmethod
    def filter(cls, **kwargs):
        query = cls.query.filter_by(**kwargs)
        return query.all()
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self.save()
    
    def delete(self):
        db.session.delete(self)
        return db.session.commit()
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self


class Model(db.Model, CRUDMixin):
    __abstract__ = True
    __table_args__ = {"extend_existing": True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    create_date = Column("create_date", TIMESTAMP, default=func.now())
    edit_date = Column("edit_date", TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())

    @classmethod
    def exists(cls, ent_id):
        result = cls.query.get(ent_id)
        return result is not None
    
    def __str__(self):
        return f"id = {self.id}"
    
    def __repr__(self):
        return f"id = {self.id}"
