from pydantic import BaseModel, constr


class CreateUserTokenSchema(BaseModel):
    email: constr(max_length=50)  # type: ignore
    password: str


class CreateAdvertisementSchema(BaseModel):
    title: constr(max_length=50)  # type: ignore
    description: constr(max_length=100)  # type: ignore


class PartialUpdateAdvertisementSchema(BaseModel):
    title: constr(max_length=50) | None = None  # type: ignore
    description: constr(max_length=100) | None = None  # type: ignore
