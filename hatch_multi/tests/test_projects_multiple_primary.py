from os import listdir
from pathlib import Path
from shutil import rmtree
from subprocess import check_call
from sys import executable
from zipfile import ZipFile


def test_project_basic_multiple_primary():
    project = "test_project_multiple_primary"
    try:
        rmtree(f"hatch_multi/tests/{project}/dist")
    except FileNotFoundError:
        pass

    check_call(
        [
            executable,
            "-m",
            "build",
            "-n",
            "-w",
        ],
        cwd=f"hatch_multi/tests/{project}",
        env={"SKIP_HATCH_MULTI": "1"},
    )

    assert Path(f"hatch_multi/tests/{project}/dist").exists()
    assert listdir(f"hatch_multi/tests/{project}/dist") == ["hatch_cpp_test_project_basic-0.1.0-py3-none-any.whl"]
    with ZipFile(f"hatch_multi/tests/{project}/dist/hatch_cpp_test_project_basic-0.1.0-py3-none-any.whl", "r") as zip_ref:
        zip_ref.extractall(f"hatch_multi/tests/{project}/dist/extracted")
    assert (
        Path(f"hatch_multi/tests/{project}/dist/extracted").joinpath("hatch_cpp_test_project_basic-0.1.0.dist-info/METADATA").read_text()
        == """Metadata-Version: 2.4
Name: hatch-cpp-test-project-basic
Version: 0.1.0
Dynamic: Requires-Dist
Summary: Basic test project for hatch-cpp
Requires-Python: >=3.11
Provides-Extra: main
Requires-Dist: superstore; extra == 'main'
Provides-Extra: other
Requires-Dist: organizeit2; extra == 'other'
"""
    )
    rmtree(f"hatch_multi/tests/{project}/dist")

    check_call(
        [
            executable,
            "-m",
            "build",
            "-n",
            "-w",
        ],
        cwd=f"hatch_multi/tests/{project}",
    )

    assert Path(f"hatch_multi/tests/{project}/dist").exists()
    assert listdir(f"hatch_multi/tests/{project}/dist") == ["hatch_cpp_test_project_basic-0.1.0-py3-none-any.whl"]
    with ZipFile(f"hatch_multi/tests/{project}/dist/hatch_cpp_test_project_basic-0.1.0-py3-none-any.whl", "r") as zip_ref:
        zip_ref.extractall(f"hatch_multi/tests/{project}/dist/extracted")
    assert (
        Path(f"hatch_multi/tests/{project}/dist/extracted").joinpath("hatch_cpp_test_project_basic-0.1.0.dist-info/METADATA").read_text()
        == """Metadata-Version: 2.4
Name: hatch-cpp-test-project-basic
Version: 0.1.0
Summary: Basic test project for hatch-cpp
Requires-Python: >=3.11
Requires-Dist: organizeit2
Requires-Dist: superstore
Provides-Extra: main
Requires-Dist: superstore; extra == 'main'
Provides-Extra: other
Requires-Dist: organizeit2; extra == 'other'
"""
    )
    rmtree(f"hatch_multi/tests/{project}/dist")

    check_call(
        [
            executable,
            "-m",
            "build",
            "-n",
            "-w",
        ],
        cwd=f"hatch_multi/tests/{project}",
        env={"HATCH_MULTI_BUILD": "other"},
    )

    assert Path(f"hatch_multi/tests/{project}/dist").exists()
    assert listdir(f"hatch_multi/tests/{project}/dist") == ["hatch_cpp_test_project_basic_other-0.1.0-py3-none-any.whl"]
    with ZipFile(f"hatch_multi/tests/{project}/dist/hatch_cpp_test_project_basic_other-0.1.0-py3-none-any.whl", "r") as zip_ref:
        zip_ref.extractall(f"hatch_multi/tests/{project}/dist/extracted")
    assert (
        Path(f"hatch_multi/tests/{project}/dist/extracted").joinpath("hatch_cpp_test_project_basic_other-0.1.0.dist-info/METADATA").read_text()
        == """Metadata-Version: 2.4
Name: hatch-cpp-test-project-basic-other
Version: 0.1.0
Summary: Basic test project for hatch-cpp
Requires-Python: >=3.11
Requires-Dist: organizeit2
Provides-Extra: main
Requires-Dist: superstore; extra == 'main'
"""
    )
    rmtree(f"hatch_multi/tests/{project}/dist")
