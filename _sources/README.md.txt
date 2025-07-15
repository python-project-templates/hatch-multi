# hatch multi

Create multiple discrete packages from optional-dependencies (extras)

[![Build Status](https://github.com/python-project-templates/hatch-multi/actions/workflows/build.yaml/badge.svg?branch=main&event=push)](https://github.com/python-project-templates/hatch-multi/actions/workflows/build.yaml)
[![codecov](https://codecov.io/gh/python-project-templates/hatch-multi/branch/main/graph/badge.svg)](https://codecov.io/gh/python-project-templates/hatch-multi)
[![License](https://img.shields.io/github/license/python-project-templates/hatch-multi)](https://github.com/python-project-templates/hatch-multi)
[![PyPI](https://img.shields.io/pypi/v/hatch-multi.svg)](https://pypi.python.org/pypi/hatch-multi)

## Overview

A small [hatch plugin](https://hatch.pypa.io/latest/) to create multiple discrete packages from a single package, via `optional-dependencies`.

**pyproject.toml**

```toml
[project]
name = "my-project"
...
dynamic = ["dependencies"]

[project.optional-dependencies]
main = [...]
other = [...]

[tool.hatch.metadata.hooks.multi]
primary = "main"
```

```bash
python -m build
# Produces my-project wheel and sdist, with dependencies from [project.optional-dependencies.main]

HATCH_MULTI_BUILD=other python -m build
# Produces my-project-other wheel and sdist, with dependencies from [project.optional-dependencies.other]
```



> [!NOTE]
> This library was generated using [copier](https://copier.readthedocs.io/en/stable/) from the [Base Python Project Template repository](https://github.com/python-project-templates/base).
