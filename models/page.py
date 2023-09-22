from sqlalchemy import (
    Column,
    Boolean,
    Integer,
    BigInteger,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from db.base_class import Base


class Page(Base):
    __tablename__ = 'pages'

    id = Column(BigInteger, primary_key=True, index=True)
    page = Column(JSONB)
    page_order = Column(Integer)
    deleted = Column(Boolean, default=False)

    document_id = Column(BigInteger, ForeignKey('documents.id'))

    document = relationship('Document', back_populates='pages')
    fields = relationship('Field', back_populates='page', cascade='all, delete-orphan')
