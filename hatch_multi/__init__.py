__version__ = "1.0.0"

from .hooks import hatch_register_build_hook, hatch_register_metadata_hook
from .plugin import HatchMultiBuildHook, HatchMultiMetadataHook
from .structs import *
