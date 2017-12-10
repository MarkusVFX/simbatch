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


def test_get_none_index_from_id(sib):
    assert sib.t.get_index_by_id(2) is None


def test_load_tasks_from_json(sib):
    json_file = sib.s.store_data_json_directory + sib.s.JSON_TASKS_FILE_NAME
    assert sib.comfun.file_exists(json_file) is True
    assert sib.t.load_tasks_from_json(json_file=json_file) is True
    assert sib.t.total_tasks == sib.t.sample_data_total


def test_get2_index_from_id(sib):
    assert sib.t.get_index_by_id(2) == 1


def test_load_schemas(sib):
    assert sib.t.clear_all_tasks_data() is True
    assert sib.t.total_tasks == 0
    assert sib.t.load_tasks() is True


def test_get3_index_from_id(sib):
    assert sib.t.get_index_by_id(2) == 1
    assert sib.t.get_index_by_id(3) == 2


def test_total_tasks(sib):
    assert sib.t.total_tasks == sib.t.sample_data_total
    assert len(sib.t.tasks_data) == sib.t.sample_data_total


def test_update_current_from_id(sib):
    assert sib.t.current_task_id is None
    assert sib.t.current_task_index is None
    assert sib.t.update_current_from_id(2) == 1
    assert sib.t.current_task_id == 2
    assert sib.t.current_task_index == 1
    assert sib.t.current_task.task_name == "tsk 2"


def test_update_current_from_index(sib):
    sib.t.current_task_id = None
    sib.t.current_task_index = None
    assert sib.t.update_current_from_index(2) == 3
    assert sib.t.current_task_id == 3
    assert sib.t.current_task_index == 2
    assert sib.t.current_task.task_name == "tsk 3"


def test_current_task_details(sib):
    assert sib.t.current_task.id == 3
    assert sib.t.current_task.task_name == "tsk 3"
    assert sib.t.current_task.state_id == 1
    assert sib.t.current_task.state == "INIT"
    assert sib.t.current_task.project_id == 2
    assert sib.t.current_task.schema_id == 1
    assert sib.t.current_task.sequence == "02"
    assert sib.t.current_task.shot == "004"
    assert sib.t.current_task.take == "b"
    assert sib.t.current_task.sim_frame_start == 7
    assert sib.t.current_task.sim_frame_end == 28
    assert sib.t.current_task.prev_frame_start == 8
    assert sib.t.current_task.prev_frame_end == 22
    assert sib.t.current_task.schema_ver == 4
    assert sib.t.current_task.task_ver == 5
    assert sib.t.current_task.queue_ver == 6
    assert sib.t.current_task.options == "o"
    assert sib.t.current_task.user_id == 1
    assert sib.t.current_task.priority == 8
    assert sib.t.current_task.description == "d"


def test_remove_single_schema_by_id(sib):
    assert sib.t.remove_single_task(id=1) is True
    assert sib.t.total_tasks == 4
    assert len(sib.t.tasks_data) == 4

def test_remove_single_schema_by_index(sib):
    assert sib.t.remove_single_task(index=1) is True
    assert sib.t.total_tasks == 3
    assert len(sib.t.tasks_data) == 3



