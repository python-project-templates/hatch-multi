from __future__ import annotations

from json import dumps
from logging import getLogger
from os import getenv
from pathlib import Path
from tempfile import NamedTemporaryFile

from hatchling.builders.hooks.plugin.interface import BuildHookInterface
from hatchling.metadata.plugin.interface import MetadataHookInterface

from .structs import HatchMultiConfig

__all__ = ("HatchMultiBuildHook", "HatchMultiMetadataHook")


class HatchMultiBuildHook(BuildHookInterface):
    """The hatch-multi build hook."""

    PLUGIN_NAME = "hatch-multi"
    _temporary_project_file: Path | None = None

    def initialize(self, version: str, build_data: dict) -> None:
        if self.target_name != "sdist":
            return

        configured_name = self.metadata.config["project"]["name"]
        package_name = self.metadata.core.raw_name
        if package_name == configured_name:
            return

        project_file = Path(self.root, "pyproject.toml")
        lines = project_file.read_text(encoding="utf-8").splitlines(keepends=True)
        in_project_table = False
        for index, line in enumerate(lines):
            stripped_line = line.strip()
            if stripped_line.startswith("[") and stripped_line.endswith("]"):
                in_project_table = stripped_line == "[project]"
            elif in_project_table:
                key, separator, _value = line.partition("=")
                if separator and key.strip() == "name":
                    newline = "\n" if line.endswith("\n") else ""
                    lines[index] = f"{key}= {dumps(package_name)}{newline}"
                    break

        with NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".toml", delete=False) as temporary_project_file:
            temporary_project_file.writelines(lines)
            self._temporary_project_file = Path(temporary_project_file.name)

        build_data["force_include"].pop(str(project_file), None)
        build_data["force_include"][str(self._temporary_project_file)] = "pyproject.toml"

    def finalize(self, version: str, build_data: dict, artifact_path: str) -> None:
        if self._temporary_project_file is not None:
            self._temporary_project_file.unlink()
            self._temporary_project_file = None


class HatchMultiMetadataHook(MetadataHookInterface):
    """The hatch-multi metadata hook."""

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
                if isinstance(config.primary, list):
                    metadata["dependencies"] = [dep for extra in config.primary for dep in metadata["optional-dependencies"].get(extra, [])]
                else:
                    metadata["dependencies"] = metadata["optional-dependencies"].get(config.primary, [])
            else:
                self._logger.info("Setting metadata for default dependency set in hatch-multi")
                # If no primary is set, use the first extra as default
                if metadata["optional-dependencies"]:
                    first_extra = next(iter(metadata["optional-dependencies"]))
                    metadata["dependencies"] = metadata["optional-dependencies"].get(first_extra, [])
                else:
                    metadata["dependencies"] = []
