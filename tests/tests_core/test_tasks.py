from simbatch.core import core as batch
import pytest

@pytest.fixture(scope="module")
def sib():
    # TODO pytest-datadir pytest-datafiles      vs       (   path.dirname( path.realpath(sys.argv[0]) )
    sib = batch.SimBatch(5, ini_file="S:/simbatch/tests/config_tests.ini")
    return sib


def test_prepare_data_directory_by_delete_all_files(sib):
    assert sib.s.store_data_mode is not None
    if sib.s.store_data_mode == 1:
        assert sib.comfun.path_exists(sib.s.store_data_json_directory) is True
    else:
        # PRO version with sql
        pass
    sib.t.clear_all_tasks_data(clear_stored_data=True)


def test_no_task_data(sib):
    assert len(sib.s.store_data_json_directory) > 0
    assert len(sib.s.JSON_TASKS_FILE_NAME) > 0
    assert sib.comfun.file_exists(sib.s.store_data_json_directory + sib.s.JSON_TASKS_FILE_NAME) is False


def test_create_example_tasks_data(sib):
    assert sib.t.create_example_tasks_data(do_save=True) == sib.t.sample_data_checksum
    assert sib.t.sample_data_checksum is not None
    assert sib.t.sample_data_total is not None
    assert sib.t.total_tasks == sib.t.sample_data_total


def test_exist_proj_data(sib):
    assert sib.comfun.file_exists(sib.s.store_data_json_directory + sib.s.JSON_TASKS_FILE_NAME) is True


def test_clear_all_tasks_data(sib):
    assert sib.t.clear_all_tasks_data() is True
    assert sib.t.total_tasks == 0
    assert len(sib.t.tasks_data) == 0


def test_json_schemas_data(sib):
    assert sib.s.store_data_mode is not None
    if sib.s.store_data_mode == 1:
        json_file = sib.s.store_data_json_directory + sib.s.JSON_TASKS_FILE_NAME
        json_tasks = sib.comfun.load_json_file(json_file)
        json_keys = json_tasks.keys()
        assert ("tasks" in json_keys) is True

