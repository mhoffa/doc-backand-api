from sqlalchemy import (
    Text,
    Float,
    Column,
    Integer,
    Boolean,
    ForeignKey,
    BigInteger,
)

from sqlalchemy.orm import relationship

from db.base_class import Base


class Document(Base):
    __tablename__ = 'documents'

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    document_type = Column(Text, nullable=False)
    file_uri = Column(Text)

    dpi = Column(Integer, nullable=False)
    deleted = Column(Boolean, default=False)
    created_at = Column(BigInteger, nullable=False)
    updated_at = Column(BigInteger, nullable=False)
    priority = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False)
    conf = Column(Float, nullable=False)
    revision = Column(Boolean, default=False)

    user_id = Column(BigInteger)
    package_id = Column(BigInteger, ForeignKey('packages.id'))

    package = relationship('Package', back_populates='documents')
    pages = relationship('Page', back_populates='document', cascade='all, delete-orphan')
