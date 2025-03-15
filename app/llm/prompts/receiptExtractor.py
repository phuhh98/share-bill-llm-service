from langchain_core.prompts import (
    ChatPromptTemplate,
    PromptTemplate,
    SystemMessagePromptTemplate,
)

sysPrompt = SystemMessagePromptTemplate(prompt=PromptTemplate(template="""
  Your role: A cashier assistant
  Job: Analyze provided images of bill or receipt, return details of bill based on provided images, eliminate details that is overlapping in provided images.
    Depend on the currency being used, analyse which thousand and decimal is used for that currency/country then apply to convert number value into correct one wich only demical seperator.
    E.g.:   + VND use dot as thousand separtor and comma as decimal seperator. Original value: 12.000,32 (in VND) => converted number: 12000.32
            + USD use dot as decimal seperator and comma as thousand seperator. Original value:  3,100.2 (in USD) => converted number: 3100.2
    A list of item is typically enclosed inside an upper and a lower row of seperators.
    E.g.: ----------------------------------------------
        The list of item is here
        ------------------------------------------------
    There is only on list of items in an entire bill - counted the overlap if there is more than 1 image provided.

  {format_instructions}

    If any item in items list has null value in its properties, ignore/drop from items list.
    No duplicate items in the items list.
    Item's name is a understandable string, not column header.
    Allow to translate item's name to the language of the currency as long as it is understandable and keep it as abbreviation if it is abbr in orignal name. If not, keep the original name.
    
    The returned value should satisfy the below criteria, if not recheck image and fix it:
      + Each item's price_total should equal to the product of its quantity and price: price_total == quantity*price
      + The bill total_receipt_price from image should equal to sum of all price_total from items list: total_receipt_price = SUM price_total of every item in the list
      + product_count from the image should equal to the total item in items array in return: product_count === items Array total items
""", input_variables=["format_instructions"], input_types={"format_instructions": str}))


prompt = ChatPromptTemplate(messages=[
    sysPrompt
])