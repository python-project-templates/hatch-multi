from __future__ import annotations

from logging import getLogger
from os import getenv

from hatchling.metadata.plugin.interface import MetadataHookInterface

from .structs import HatchMultiConfig

__all__ = ("HatchMultiMetadataHook",)


class HatchMultiMetadataHook(MetadataHookInterface):
    """The hatch-multi build hook."""

    PLUGIN_NAME = "hatch-multi"
    _logger = getLogger(__name__)

    def update(self, metadata: dict) -> None:
        # Skip if SKIP_HATCH_MULTI is set
        # TODO: Support CLI once https://github.com/pypa/hatch/pull/1743
        if getenv("SKIP_HATCH_MULTI"):
            self._logger.info("Skipping the metadata hook since SKIP_HATCH_MULTI was set")
            return

        # TODO: make CLI after https://github.com/pypa/hatch/pull/1743
        extra = getenv("HATCH_MULTI_BUILD")

        config = HatchMultiConfig.model_validate(dict(name=metadata["name"], **self.config))

        if extra and extra in metadata["optional-dependencies"]:
            self._logger.info(f"Setting metadata for extra '{extra}' in hatch-multi")
            metadata["name"] = f"{config.name}-{extra}"
            metadata["dependencies"] = metadata["optional-dependencies"].pop(extra)
        else:
            metadata["name"] = config.name
            if config.primary:
                self._logger.info(f"Setting metadata for primary dependency set '{config.primary}' in hatch-multi")
                metadata["dependencies"] = metadata["optional-dependencies"].get(config.primary, [])
            else:
                self._logger.info("Setting metadata for default dependency set in hatch-multi")
                # If no primary is set, use the first extra as default
                if metadata["optional-dependencies"]:
                    first_extra = next(iter(metadata["optional-dependencies"]))
                    metadata["dependencies"] = metadata["optional-dependencies"].get(first_extra, [])
                else:
                    metadata["dependencies"] = []
