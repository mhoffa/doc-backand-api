from sqlalchemy import (
    event,
    inspect,
)
from sqlalchemy.orm import (
    Mapper,
    class_mapper,
)
from sqlalchemy.orm.attributes import get_history


from core.entities import AuditActions


class AuditableMixin:
    @staticmethod
    def create_audit(connection, object_type, object_id, action, **kwargs):
        from models import AuditLog

        audit = AuditLog(
            target_type=object_type,
            target_id=object_id,
            action_type=action,
            user_id=kwargs.get('user_id'),
            state_before=kwargs.get('state_before'),
            state_after=kwargs.get('state_after')
        )
        audit.save(connection)

    @classmethod
    def __declare_last__(cls):
        event.listen(cls, 'after_insert', cls.insert)
        event.listen(cls, 'after_delete', cls.delete)
        event.listen(cls, 'after_update', cls.update)

    @classmethod
    def get_primary_key(cls, model: any) -> int | None:
        name_primary_key = [c.key for c in model.__table__.c if c.primary_key]
        if name_primary_key:
            return getattr(model, name_primary_key[0])
        return None

    @classmethod
    def insert(cls, mapper: Mapper, connection: any, target: any) -> None:
        target.create_audit(
            connection,
            target.__tablename__,
            cls.get_primary_key(target),
            AuditActions.CREATE.value,
            user_id=getattr(target, '_sid'),
        )

    @classmethod
    def delete(cls, mapper: Mapper, connection: any, target: any) -> None:
        target.create_audit(
            connection,
            target.__tablename__,
            cls.get_primary_key(target),
            AuditActions.DELETE.value,
            user_id=getattr(target, '_sid', None),
        )

    @classmethod
    def update(cls, mapper: Mapper, connection: any, target: any) -> None:
        state_after: dict = {}
        state_before: dict = {}

        inspector = inspect(target)
        attrs = class_mapper(target.__class__).column_attrs

        for attr in attrs:
            obj_history = getattr(inspector.attrs, attr.key).history
            if obj_history.has_changes():
                state_after[attr.key] = getattr(target, attr.key)
                state_before[attr.key] = get_history(target, attr.key)[2].pop()

        if state_before and state_after:
            target.create_audit(
                connection,
                target.__tablename__,
                cls.get_primary_key(target),
                AuditActions.UPDATE.value,
                user_id=getattr(target, '_sid'),
                state_before=state_before,
                state_after=state_after
            )
