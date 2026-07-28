from hatchling.plugin import hookimpl

from .plugin import HatchMultiBuildHook, HatchMultiMetadataHook


@hookimpl
def hatch_register_build_hook() -> type[HatchMultiBuildHook]:
    return HatchMultiBuildHook


@hookimpl
def hatch_register_metadata_hook() -> type[HatchMultiMetadataHook]:
    return HatchMultiMetadataHook
