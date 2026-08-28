from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, EmailStr, StringConstraints

NullableString = Annotated[str | None, StringConstraints(max_length=100)]

NullableEmailString = Annotated[
    EmailStr | Literal[""] | None, StringConstraints(max_length=255)
]


class StrictMode(BaseModel):
    model_config = ConfigDict(strict=True)
