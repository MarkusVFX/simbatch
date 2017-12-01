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
    sib.c.clear_all_schemas_data(clear_stored_data=True)


def test_no_schema_data(sib):
    assert sib.comfun.file_exists(sib.s.store_data_json_directory + sib.s.JSON_SCHEMAS_FILE_NAME) is False


def test_create_example_schemas_data(sib):
    assert sib.c.create_example_schemas_data(do_save=True) == 10
    assert sib.c.total_schemas == 4


def test_exist_proj_data(sib):
    assert sib.comfun.file_exists(sib.s.store_data_json_directory + sib.s.JSON_SCHEMAS_FILE_NAME) is True


def test_clear_all_schemas_data(sib):
    assert sib.c.clear_all_schemas_data() is True
    assert sib.c.total_schemas == 0
    assert len(sib.c.schemas_data) == 0



def test_json_schemas_data(sib):
    assert sib.s.store_data_mode is not None
    if sib.s.store_data_mode == 1:
        json_file = sib.s.store_data_json_directory + sib.s.JSON_SCHEMAS_FILE_NAME
        json_schemas = sib.comfun.load_json_file(json_file)
        jskon_keys = json_schemas.keys()
        assert ("schemas" in jskon_keys) is True


def test_get_none_index_from_id(sib):
    assert sib.p.get_index_from_id(2) is None


def test_load_schemas_from_json(sib):
    json_file = sib.s.store_data_json_directory + sib.s.JSON_SCHEMAS_FILE_NAME
    assert sib.c.load_schemas_from_json(json_file=json_file) is True

def test_get2_index_from_id(sib):
    assert sib.c.get_schema_index_by_id(2) == 1

def test_load_schemas(sib):
    assert sib.c.clear_all_schemas_data() is True
    assert sib.c.load_schemas() is True

def test_get3_index_from_id(sib):
    assert sib.c.get_schema_index_by_id(3) == 2


def test_total_schemas(sib):
    assert sib.c.total_schemas == 4
    assert len(sib.c.schemas_data) == 4


def test_update_current_from_id(sib):
    assert sib.c.current_schema_id is None
    assert sib.c.current_schema_index is None
    assert sib.c.update_current_from_id(2) == 1
    # sib.p.print_all()
    assert sib.c.current_schema_id == 2
    assert sib.c.current_schema_index == 1
    assert sib.c.current_schema.schema_name == "schema 2"


def test_update_current_from_index(sib):
    sib.c.current_schema_id = None
    sib.c.current_schema_index = None
    assert sib.c.update_current_from_index(2) == 3
    assert sib.c.current_schema_id == 3
    assert sib.c.current_schema_index == 2
    assert sib.c.current_schema.schema_name == "schema 3"


def test_schema_item_details(sib):
    assert sib.c.current_schema.id == 3
    assert sib.c.current_schema.schema_name == "schema 3"
    assert sib.c.current_schema.state_id == 22
    assert sib.c.current_schema.state == "ACTIVE"
    assert sib.c.current_schema.schema_version == 22
    assert sib.c.current_schema.project_id == 2
    assert sib.c.current_schema.project_name == "proj2"
    assert sib.c.current_schema.definition_id == 2
    assert len(sib.c.current_schema.actions_array) == 0
    assert sib.c.current_schema.description == "fire with smoke"


def test_remove_single_schema(sib):
    assert sib.c.remove_single_schema(id=1) is True
    assert sib.c.total_schemas == 3
    assert len(sib.c.schemas_data) == 3
    assert sib.c.remove_single_schema(index=1) is True
    assert sib.c.total_schemas == 2
    assert len(sib.c.schemas_data) == 2


#def test_empty1_clear_all_projects_data(schemas):
    #assert proj.clear_all_projects_data() is True
