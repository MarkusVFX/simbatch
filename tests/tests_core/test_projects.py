# import sys
# from os import path
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
    sib.p.clear_all_projects_data(clear_stored_data=True)


def test_no_proj_data(sib):
    assert sib.comfun.file_exists(sib.s.store_data_json_directory + sib.s.JSON_PROJECTS_FILE_NAME) is False


def test_create_example_project_data(sib):
    assert sib.p.create_example_project_data(do_save=True) == sib.p.sample_data_checksum
    assert sib.p.sample_data_checksum is not None
    assert sib.p.total_projects == sib.p.sample_data_total


def test_exist_proj_data(sib):
    assert sib.comfun.file_exists(sib.s.store_data_json_directory + sib.s.JSON_PROJECTS_FILE_NAME) is True


def test_clear_all_projects_data(sib):
    assert sib.p.clear_all_projects_data() is True
    assert sib.p.total_projects == 0
    assert len(sib.p.projects_data) == 0


def test_json_projects_data(sib):
    assert sib.s.store_data_mode is not None
    if sib.s.store_data_mode == 1:
        json_file = sib.s.store_data_json_directory + sib.s.JSON_PROJECTS_FILE_NAME
        json_projects = sib.comfun.load_json_file(json_file)
        jskon_keys = json_projects.keys()
        assert ("projects" in jskon_keys) is True


def test_get_none_index_from_id(sib):
    assert sib.p.get_index_from_id(2) is None


def test_load_projects(sib):
    assert sib.p.clear_all_projects_data() is True
    assert sib.p.load_projects() is True


def test_get_index_from_id(sib):
    assert sib.p.get_index_from_id(2) == 1


def test_total_projects(sib):
    assert sib.p.total_projects == 3
    assert len(sib.p.projects_data) == 3


def test_update_current_from_id(sib):
    assert sib.p.current_project_id is None
    assert sib.p.current_project_index is None
    assert sib.p.update_current_from_id(2) is True
    # sib.p.print_all()
    assert sib.p.current_project_id == 2
    assert sib.p.current_project_index == 1


def test_update_current_from_index(sib):
    sib.p.current_project_id = None
    sib.p.current_project_index = None
    assert sib.p.update_current_from_index(2) is True
    assert sib.p.current_project_id == 3
    assert sib.p.current_project_index == 2


def test_check_is_default(sib):
    assert sib.p.check_is_default(index=1) is False
    assert sib.p.check_is_default(index=2) is True


def test_by_id_set_proj_as_default(sib):
    assert sib.p.set_proj_as_default(id=1) is True
    index = sib.p.get_index_from_id(1)
    assert sib.p.check_is_default(index=index) is True
    assert sib.p.set_proj_as_default(id=2) is True
    index = sib.p.get_index_from_id(2)
    assert sib.p.check_is_default(index=index) is True


def test_by_index_set_proj_as_default(sib):
    assert sib.p.set_proj_as_default(index=0) is True
    assert sib.p.check_is_default(index=0) is True
    assert sib.p.set_proj_as_default(index=1) is True
    assert sib.p.check_is_default(index=1) is True


def test_init_default_proj(sib):
    assert sib.p.current_project_id == 3
    assert sib.p.current_project_index == 2
    sib.p.init_default_proj()
    assert sib.p.current_project_id == 2
    assert sib.p.current_project_index == 1


def test_remove_single_project(sib):
    assert sib.p.remove_single_project(id=1) is True
    assert sib.p.total_projects == 2
    assert len(sib.p.projects_data) == 2
    assert sib.p.remove_single_project(index=1) is True
    assert sib.p.total_projects == 1
    assert len(sib.p.projects_data) == 1


def test_empty2_clear_all_projects_data(sib):
    assert sib.p.clear_all_projects_data() is True
    assert sib.p.total_projects == 0
    assert len(sib.p.projects_data) == 0

def test_save_projects_to_json(sib):
    # assert sib.p.save_projects_to_json() == True
    pass

# def test_get_dir_patterns(sib):   # TODO
