from __future__ import annotations

from typing import Optional

from pydantic import AliasChoices, BaseModel, Field

__all__ = ("HatchMultiConfig",)


class HatchMultiConfig(BaseModel, validate_assignment=True):
    name: str = Field(description="Name of the package")
    primary: Optional[str] = Field(
        default=None,
        description="Optional dependecy set to use as primary",
        alias=AliasChoices("primary", "default"),
    )
