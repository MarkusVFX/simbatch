from simbatch.core import core as batch
from simbatch.core.actions import SingleAction

import pytest
import os


@pytest.fixture(scope="module")
def sib():
    # TODO pytest-datadir pytest-datafiles      vs       (   path.dirname( path.realpath(sys.argv[0]) )
    settings_file = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep + "config_tests.ini"
    sib = batch.SimBatch(5, ini_file=settings_file)
    return sib


def test_prepare_data_directory_by_delete_all_files(sib):
    assert sib.sts.store_data_mode is not None
    if sib.sts.store_data_mode == 1:
        assert sib.comfun.path_exists(sib.sts.store_data_json_directory_abs) is True
    else:
        # PRO version with sql
        pass
    # sib.sch.clear_all_schemas_data(clear_stored_data=True)
    sib.sch.delete_json_schema_file()


def test_no_schema_data(sib):
    assert len(sib.sts.store_data_json_directory_abs) > 0
    assert len(sib.sts.JSON_SCHEMAS_FILE_NAME) > 0
    assert sib.comfun.file_exists(sib.sts.store_data_json_directory_abs + sib.sts.JSON_SCHEMAS_FILE_NAME) is False


def test_create_example_schemas_data(sib):
    assert sib.sch.create_example_schemas_data(do_save=True) == sib.sch.sample_data_checksum
    assert sib.sch.sample_data_checksum is not None
    assert sib.sch.sample_data_total is not None
    assert sib.sch.total_schemas == sib.sch.sample_data_total


def test_exist_proj_data(sib):
    assert sib.comfun.file_exists(sib.sts.store_data_json_directory_abs + sib.sts.JSON_SCHEMAS_FILE_NAME) is True


def test_clear_all_schemas_data(sib):
    assert sib.sch.clear_all_schemas_data() is True
    assert sib.sch.total_schemas == 0
    assert len(sib.sch.schemas_data) == 0


def test_json_schemas_data(sib):
    assert sib.sts.store_data_mode is not None
    if sib.sts.store_data_mode == 1:
        json_file = sib.sts.store_data_json_directory_abs + sib.sts.JSON_SCHEMAS_FILE_NAME
        json_schemas = sib.comfun.load_json_file(json_file)
        json_keys = json_schemas.keys()
        assert ("schemas" in json_keys) is True


def test_get_none_index_from_id(sib):
    assert sib.sch.get_index_by_id(2) is None


def test_load_schemas_from_json(sib):
    json_file = sib.sts.store_data_json_directory_abs + sib.sts.JSON_SCHEMAS_FILE_NAME
    assert sib.comfun.file_exists(json_file) is True
    assert sib.sch.load_schemas_from_json(json_file=json_file) is True
    assert sib.sch.total_schemas == sib.sch.sample_data_total


def test_get2_index_from_id(sib):
    assert sib.sch.get_index_by_id(2) == 1


def test_load_schemas(sib):
    assert sib.sch.clear_all_schemas_data() is True
    assert sib.sch.total_schemas == 0
    assert sib.sch.load_schemas() is True


def test_get3_index_from_id(sib):
    assert sib.sch.get_index_by_id(3) == 2


def test_total_schemas(sib):
    assert sib.sch.total_schemas == sib.sch.sample_data_total
    assert len(sib.sch.schemas_data) == sib.sch.sample_data_total


def test_update_current_from_id(sib):
    assert sib.sch.current_schema_id is None
    assert sib.sch.current_schema_index is None
    assert sib.sch.update_current_from_id(2) == 1
    # sib.prj.print_all()
    assert sib.sch.current_schema_id == 2
    assert sib.sch.current_schema_index == 1
    assert sib.sch.current_schema.schema_name == "schema 2"


def test_update_current_from_index(sib):
    sib.sch.current_schema_id = None
    sib.sch.current_schema_index = None
    assert sib.sch.update_current_from_index(2) == 3
    assert sib.sch.current_schema_id == 3
    assert sib.sch.current_schema_index == 2
    assert sib.sch.current_schema.schema_name == "schema 3"


def test_current_schema_details(sib):
    assert sib.sch.current_schema.id == 3
    assert sib.sch.current_schema.schema_name == "schema 3"
    assert sib.sch.current_schema.state_id == 22
    assert sib.sch.current_schema.state == "ACTIVE"
    assert sib.sch.current_schema.schema_version == 5
    assert sib.sch.current_schema.project_id == 2
    assert sib.sch.current_schema.based_on_definition == "virtual_definition"
    assert len(sib.sch.current_schema.actions_array) > 0   # TODO precise
    assert sib.sch.current_schema.description == "fire with smoke"


def test_remove_single_schema_by_id(sib):
    assert sib.sch.remove_single_schema(sch_id=1) is True
    assert sib.sch.total_schemas == 3
    assert len(sib.sch.schemas_data) == 3


def test_remove_single_schema_by_index(sib):
    assert sib.sch.remove_single_schema(index=1) is True
    assert sib.sch.total_schemas == 2
    assert len(sib.sch.schemas_data) == 2


def test_actions_in_single_schema(sib):
    assert sib.sch.total_schemas == 2
    assert len(sib.sch.schemas_data) == 2


def test_add_schema(sib):
    assert len(sib.sch.current_schema.actions_array) == 1
    # sia = SingleAction(-1, "virtual action", "virt descr", "<val>", "template <f>", type="single", ui=(("ui", "2+2")))
    sia = SingleAction("virtual action", "virt descr", "template <f>", mode="single", ui=(("ui", "2+2")))
    sib.sch.current_schema.add_action_to_schema(sia)
    assert len(sib.sch.current_schema.actions_array) == 2


def test_print_current(sib):
    sib.sch.print_current()


def test_print_all(sib):
    sib.sch.print_all()
