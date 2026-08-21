from typing import Annotated, Literal

from pydantic import EmailStr, StringConstraints

NullableString = Annotated[str | None, StringConstraints(max_length=100)]

NullableEmailString = Annotated[
    EmailStr | Literal[""] | None, StringConstraints(max_length=255)
]
