from __future__ import annotations

from pydantic import AliasChoices, BaseModel, Field

__all__ = ("HatchMultiConfig",)


class HatchMultiConfig(BaseModel, validate_assignment=True):
    name: str = Field(description="Name of the package")
    primary: str | list[str] | None = Field(
        default=None,
        description="Optional dependency set/s to use as primary",
        alias=AliasChoices("primary", "default"),
    )
