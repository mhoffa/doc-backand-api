from sqlalchemy import (
    Text,
    Time,
    Column,
    Integer,
    Boolean,
    BigInteger,
)
from sqlalchemy.orm import relationship

from db.base_class import Base


class Package(Base):
    __tablename__ = 'packages'

    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(Text, nullable=False)
    operation_type = Column(Text, nullable=False)
    operation_group = Column(Text, nullable=False)
    division_name = Column(Text, nullable=False)
    branch_name = Column(Text, nullable=False)
    district_name = Column(Text, nullable=False)
    company_name = Column(Text, nullable=False)
    ts_time = Column(Time(timezone=True), nullable=False)
    deleted = Column(Boolean, default=False)
    priority = Column(Integer, nullable=False)

    documents = relationship('Document', back_populates='package')
