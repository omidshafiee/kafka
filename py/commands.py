from pydantic import BaseModel


class CreateTransactionCommand(BaseModel):
    count: int
