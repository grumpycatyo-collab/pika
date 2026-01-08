from pydantic import BaseModel


class Commit(BaseModel):
    tree: str
    parent: str | None
    message: str
