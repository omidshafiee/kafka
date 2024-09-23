from pydantic import BaseModel


class Transaction(BaseModel):
    id: str
    date: str
    amount: str
    customer: str
