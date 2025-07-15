from typing import Type

from hatchling.plugin import hookimpl

from .plugin import HatchMultiMetadataHook


@hookimpl
def hatch_register_metadata_hook() -> Type[HatchMultiMetadataHook]:
    return HatchMultiMetadataHook
