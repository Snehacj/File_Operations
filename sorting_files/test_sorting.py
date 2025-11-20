import os
import shutil
import pytest
from script import Sorting

@pytest.fixture
def sample_config():
    return {
        "Documents": ".pdf,.doc,.txt",
        "Images": ".jpeg,.png",
        "Audio": ".mp3,.wav",
        "Videos": ".mp4,.mov"
    }

def create_file(path, name):
    file_path = os.path.join(path, name)
    with open(file_path, "w") as f:
        f.write("test")
    return file_path


def test_sorting_moves_files(tmp_path, sample_config):
    source = tmp_path / "source"
    dest = tmp_path / "dest"

    source.mkdir()
    dest.mkdir()

    # Create sample files
    create_file(source, "a.pdf")
    create_file(source, "b.mp3")
    create_file(source, "c.jpeg")

    sorter = Sorting()
    sorter.sort_files(str(source), str(dest), sample_config)

    # Verify destination structure
    assert (dest / "Documents" / "a.pdf").exists()
    assert (dest / "Audio" / "b.mp3").exists()
    assert (dest / "Images" / "c.jpeg").exists()


def test_sorting_places_unknown_in_others(tmp_path, sample_config):
    source = tmp_path / "source"
    dest = tmp_path / "dest"

    source.mkdir()
    dest.mkdir()

    create_file(source, "xyz.exe")

    sorter = Sorting()
    sorter.sort_files(str(source), str(dest), sample_config)

    assert (dest / "Others" / "xyz.exe").exists()


def test_skips_existing_file(tmp_path, sample_config):
    source = tmp_path / "source"
    dest = tmp_path / "dest"

    source.mkdir()
    dest.mkdir()

    file_name = "a.pdf"

    # File exists in source
    create_file(source, file_name)

    # And also exists in destination → should be skipped
    dest_docs = dest / "Documents"
    dest_docs.mkdir()
    create_file(dest_docs, file_name)

    sorter = Sorting()
    sorter.sort_files(str(source), str(dest), sample_config)

    # File in source should still exist (skipped)
    assert (source / file_name).exists()


def test_missing_source_folder(tmp_path, sample_config):
    source = tmp_path / "does_not_exist"
    dest = tmp_path / "dest"
    dest.mkdir()

    sorter = Sorting()
    result = sorter.sort_files(str(source), str(dest), sample_config)

    # Should not crash and not create unexpected folders
    assert not dest.joinpath("Others").exists()


def test_creates_destination_folder_if_missing(tmp_path, sample_config):
    source = tmp_path / "source"
    dest = tmp_path / "new_dest"

    source.mkdir()

    create_file(source, "a.txt")
    sorter = Sorting()
    sorter.sort_files(str(source), str(dest), sample_config)

    # Destination should be auto-created
    assert dest.exists()
    assert (dest / "Documents" / "a.txt").exists()
