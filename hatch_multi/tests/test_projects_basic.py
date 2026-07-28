from os import listdir
from pathlib import Path
from shutil import rmtree
from subprocess import check_call
from sys import executable
from tarfile import TarFile
from zipfile import ZipFile


def test_basic():
    project = "test_project_basic"
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


def test_sdist_preserves_extra():
    project = "test_project_basic"
    project_root = Path(f"hatch_multi/tests/{project}")
    rmtree(project_root / "dist", ignore_errors=True)

    check_call(
        [
            executable,
            "-m",
            "build",
            "-n",
            "-s",
        ],
        cwd=project_root,
        env={"HATCH_MULTI_BUILD": "other"},
    )

    sdist_name = "hatch_cpp_test_project_basic_other-0.1.0.tar.gz"
    assert listdir(project_root / "dist") == [sdist_name]
    with TarFile.open(project_root / "dist" / sdist_name, "r:gz") as tar_file:
        tar_file.extractall(project_root / "dist" / "extracted", filter="data")

    source_root = project_root / "dist" / "extracted" / "hatch_cpp_test_project_basic_other-0.1.0"
    check_call(
        [
            executable,
            "-m",
            "build",
            "-n",
            "-w",
        ],
        cwd=source_root,
        env={},
    )

    wheel_name = "hatch_cpp_test_project_basic_other-0.1.0-py3-none-any.whl"
    assert listdir(source_root / "dist") == [wheel_name]
    with ZipFile(source_root / "dist" / wheel_name) as zip_file:
        metadata = zip_file.read("hatch_cpp_test_project_basic_other-0.1.0.dist-info/METADATA").decode()

    assert "Name: hatch-cpp-test-project-basic-other\n" in metadata
    assert "Requires-Dist: organizeit2\n" in metadata
    rmtree(project_root / "dist")
