from typing import Annotated

from pydantic import EmailStr, StringConstraints

NullableString = Annotated[str | None, StringConstraints(min_length=1, max_length=100)]

NullableEmailString = Annotated[
    EmailStr | None, StringConstraints(min_length=1, max_length=255)
]
