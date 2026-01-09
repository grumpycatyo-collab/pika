from pydantic import BaseModel

class Commit(BaseModel):
    tree: str
    parent: str | None
    message: str

class RefValue(BaseModel):
    symbolic: bool
    value: str

