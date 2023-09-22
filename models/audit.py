from sqlalchemy import (
    func,
    Column,
    String,
    Integer,
    DateTime,
)
from sqlalchemy.dialects.postgresql import JSONB

from db.base import Base


class AuditLog(Base):
    __tablename__ = 'audit_logs'

    id = Column(Integer, primary_key=True)
    # The table name of the altered object
    target_type = Column(String(100), nullable=False)
    # The ID of the row being audited
    target_id = Column(Integer)
    # The type of action (create: 1, update: 2, delete: 3)
    action_type = Column(Integer)
    # The ID of the user who performed the action
    user_id = Column(String(42))
    # JSON representation of the state before the action
    state_before = Column(JSONB)
    # JSON representation of the state after the action
    state_after = Column(JSONB)
    created_at = Column(DateTime, default=func.current_timestamp())

    def __init__(
            self,
            target_type: str,
            action_type: int,
            user_id: str | None = None,
            target_id: int | None = None,
            state_after: dict | None = None,
            state_before: dict | None = None,
    ):
        self.action_type = action_type
        self.target_id = target_id
        self.user_id = user_id
        self.target_type = target_type
        self.state_after = state_after
        self.state_before = state_before

    def save(self, connection) -> None:
        connection.execute(
            self.__table__.insert(),
            {
                'action_type': self.action_type,
                'target_id': self.target_id,
                'user_id': self.user_id,
                'target_type': self.target_type,
                'state_after': self.state_after,
                'state_before': self.state_before,
            }
        )
