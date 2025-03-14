from typing import Union
from fastapi import APIRouter
from app.services import item as item_service, root as root_service


router = APIRouter(prefix="/root")

@router.get("/")
async def root():
    return root_service.read_root()



@router.get("/items/{item_id}")
async def item(item_id: int, q: Union[str, None] = None):
    return item_service.read_item(item_id, q)
