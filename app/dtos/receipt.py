import datetime
from typing import List, Union

from pydantic import BaseModel, Field


class BillItem(BaseModel):
    name: str = Field(description="Item's name from the image. No translation.")
    price: float = Field(description="Price of a single item")
    price_total: float = Field(description="Total price of this item")
    quantity: float = Field(description="Bought quantity of this item")


class ParsedReceipt(BaseModel):
    """Receipt details"""

    currency: str = Field(
        description="Short name of currency being used in the bill in ISO 4217 format"
    )
    error: Union[str, None] = Field(
        description="""
      Error message.
                  In case you can not process the image or the provided image is not bill or the provided image is not from a same bill,
                  return error and make joke about the situation
      """
    )
    product_count: int = Field(description="Number of unique product from the bill")
    receipt_date: datetime.date = Field(
        description="The issued date of the bill or receipt in ISO 8601 format"
    )
    total_receipt_price: float = Field(
        description="The bill total price after discount"
    )
    items: List[BillItem] = Field(description="List of bought items with details")
