from .entities import CodeErrors


def pretty_result(code: int | None = None, message: str | None = None, data: any = None) -> dict:
    if message is None:
        message = CodeErrors(code).name
    return {
        'code': code,
        'message': message,
        'data': data
    }


def get_value_from_dict_by_partial_key(data: dict, name: str) -> str | int | float | None:
    name_lower = name.lower()
    return next((v for k, v in data.items() if name_lower in k.lower()), None)


def delete_duplicate_from_list_entities(data: list[dict]) -> list[dict]:
    seen = set()
    return [item for item in data if str(item) not in seen and not seen.add(str(item))]
