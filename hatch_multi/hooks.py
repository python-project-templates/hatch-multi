from hatchling.plugin import hookimpl

from .plugin import HatchMultiMetadataHook


@hookimpl
def hatch_register_metadata_hook() -> type[HatchMultiMetadataHook]:
    return HatchMultiMetadataHook
