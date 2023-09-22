import re
import abc

from dataclasses import dataclass
from enum import (
    Enum,
    IntEnum,
)


PATTERN_SORT_FIELDS = re.compile(r'^-?[a-zA-Z0-9][a-zA-Z0-9_-]*[a-zA-Z0-9]$')

DOCUMENT_PRIORITY = {
    'low': 1,
    'middle': 2,
    'high': 3
}

DOCUMENT_STATUS = {
    'in line': 1,
    'at work': 2,
    'completed': 3
}

DOCUMENT_PRIORITY_REVERS = {
    1: 'Low',
    2: 'Middle',
    3: 'High',
}

DOCUMENT_STATUS_REVERS = {
    1: 'In line',
    2: 'At work',
    3: 'Completed',
}


class AuditActions(IntEnum):
    CREATE = 1
    UPDATE = 2
    DELETE = 3


class CodeErrors(IntEnum):
    OK = 1001
    DB_ERROR = 1002
    PARAM_ERROR = 1003
    UNKNOWN_ERROR = 1004


class EntityType(str, Enum):
    package_name = 'package_name'
    document_name = 'document_name'
    document_type = 'document_type'
    operation_type = 'operation_type'
    operation_group = 'operation_group'
    priority = 'priority'
    status = 'status'


@dataclass(frozen=True)
class AutoCompleteItem:
    label: str
    matched_field: str
    metadata: dict

    def to_dict(self) -> dict:
        return {
            'label': self.label,
            'type': self.matched_field,
            'metadata': self.metadata
        }


class MatchedFieldStrategy(abc.ABC):
    def __init__(self, field_name: str) -> None:
        self.field_name = field_name

    @abc.abstractmethod
    def process(self, data: any) -> AutoCompleteItem:
        pass


class PackageNameStrategy(MatchedFieldStrategy):
    def process(self, data: any) -> AutoCompleteItem:
        label = data.package.name
        metadata = {'package_id': data.package.id}
        return AutoCompleteItem(label, self.field_name, metadata)


class OperationTypeStrategy(MatchedFieldStrategy):
    def process(self, data: any) -> AutoCompleteItem:
        label = data.package.operation_type
        metadata = {'package_id': data.package.id}
        return AutoCompleteItem(label, self.field_name, metadata)


class OperationGroupStrategy(MatchedFieldStrategy):
    def process(self, data: any) -> AutoCompleteItem:
        label = data.package.operation_group
        metadata = {'package_id': data.package.id}
        return AutoCompleteItem(label, self.field_name, metadata)


class DocumentNameStrategy(MatchedFieldStrategy):
    def process(self, data: any) -> AutoCompleteItem:
        label = data.name
        metadata = {'document_id': data.id}
        return AutoCompleteItem(label, self.field_name, metadata)


class DocumentTypeStrategy(MatchedFieldStrategy):
    def process(self, data: any) -> AutoCompleteItem:
        label = data.document_type
        metadata = {'document_id': data.id}
        return AutoCompleteItem(label, self.field_name, metadata)


class DocumentPriorityStrategy(MatchedFieldStrategy):
    def process(self, data: any) -> AutoCompleteItem:
        label = DOCUMENT_PRIORITY_REVERS[data['priority']]
        metadata = {'priority': data['priority']}
        return AutoCompleteItem(label, self.field_name, metadata)


class DocumentStatusStrategy(MatchedFieldStrategy):
    def process(self, data: any) -> AutoCompleteItem:
        label = DOCUMENT_STATUS_REVERS[data['status']]
        metadata = {'status': data['status']}
        return AutoCompleteItem(label, self.field_name, metadata)


class AutoCompleteStrategies:
    FIELD_STRATEGIES = {
        EntityType.package_name.value: PackageNameStrategy,
        EntityType.document_name.value: DocumentNameStrategy,
        EntityType.document_type.value: DocumentTypeStrategy,
        EntityType.operation_type.value: OperationTypeStrategy,
        EntityType.operation_group.value: OperationGroupStrategy,
        EntityType.priority.value: DocumentPriorityStrategy,
        EntityType.status.value: DocumentStatusStrategy,
    }

    @classmethod
    def get(cls, data: any, field_name: str):
        strategy = cls.FIELD_STRATEGIES.get(field_name)(field_name)
        item = strategy.process(data)
        return item.to_dict()
