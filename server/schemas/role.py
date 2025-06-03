from pydantic import BaseModel


class RoleCreate(BaseModel):
    name: str
    description: str
    permission: list


class RoleUpdate(BaseModel):
    name: str
    description: str
    permission: list