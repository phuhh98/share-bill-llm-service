from typing import Union


def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}