# import sys
# from os import path
from simbatch.core import core as batch
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
    #sib.prj.clear_all_projects_data(clear_stored_data=True)
    sib.prj.delete_json_project_file()


def test_print_repr_str(sib):
    print "\n__repr__ ", repr(sib.prj)
    print "__str__ ", sib.prj


def test_no_proj_data(sib):
    assert sib.comfun.file_exists(sib.sts.store_data_json_directory_abs + sib.sts.JSON_PROJECTS_FILE_NAME) is False


def test_create_example_project_data(sib):
    assert sib.prj.create_example_project_data(do_save=True) == sib.prj.sample_data_checksum
    assert sib.prj.sample_data_checksum is not None
    assert sib.prj.total_projects == sib.prj.sample_data_total


def test_exist_proj_data(sib):
    assert sib.comfun.file_exists(sib.sts.store_data_json_directory_abs + sib.sts.JSON_PROJECTS_FILE_NAME) is True


def test_clear_all_projects_data(sib):
    assert sib.prj.clear_all_projects_data() is True
    assert sib.prj.total_projects == 0
    assert len(sib.prj.projects_data) == 0


def test_json_projects_data(sib):
    assert sib.sts.store_data_mode is not None
    if sib.sts.store_data_mode == 1:
        json_file = sib.sts.store_data_json_directory_abs + sib.sts.JSON_PROJECTS_FILE_NAME
        json_projects = sib.comfun.load_json_file(json_file)
        jskon_keys = json_projects.keys()
        assert ("projects" in jskon_keys) is True


def test_get_none_index_from_id(sib):
    assert sib.prj.get_index_from_id(2) is None


def test_load_projects(sib):
    assert sib.prj.clear_all_projects_data() is True
    assert sib.prj.load_projects() is True


def test_get_index_from_id(sib):
    assert sib.prj.get_index_from_id(2) == 1


def test_total_projects(sib):
    assert sib.prj.total_projects == 3
    assert len(sib.prj.projects_data) == 3


def test_update_current_from_id(sib):
    assert sib.prj.current_project_id is None
    assert sib.prj.current_project_index is None
    assert sib.prj.update_current_from_id(2) is True
    # sib.prj.print_all()
    assert sib.prj.current_project_id == 2
    assert sib.prj.current_project_index == 1


def test_update_current_from_index(sib):
    sib.prj.current_project_id = None
    sib.prj.current_project_index = None
    assert sib.prj.update_current_from_index(2) is True
    assert sib.prj.current_project_id == 3
    assert sib.prj.current_project_index == 2


def test_is_index2_def_projert(sib):
    assert sib.prj.check_is_default(index=0) is False
    assert sib.prj.check_is_default(index=1) is False
    assert sib.prj.check_is_default(index=2) is True


def test_by_id_set_proj_as_default(sib):
    assert sib.prj.set_proj_as_default(id=1) is True
    index = sib.prj.get_index_from_id(1)
    assert sib.prj.check_is_default(index=index) is True
    assert sib.prj.set_proj_as_default(id=2) is True
    index = sib.prj.get_index_from_id(2)
    assert sib.prj.check_is_default(index=index) is True


def test_by_index_set_proj_as_default(sib):
    assert sib.prj.set_proj_as_default(index=0) is True
    assert sib.prj.check_is_default(index=0) is True
    assert sib.prj.set_proj_as_default(index=1) is True
    assert sib.prj.check_is_default(index=1) is True
    assert sib.prj.set_proj_as_default(index=0) is True


def test_is_index0_def_projert(sib):
    assert sib.prj.check_is_default(index=0) is True
    assert sib.prj.check_is_default(index=1) is False
    assert sib.prj.check_is_default(index=2) is False


def test_init_default_proj(sib):
    assert sib.prj.current_project_id == 3
    assert sib.prj.current_project_index == 2
    sib.prj.init_default_proj()
    assert sib.prj.current_project_id == 1
    assert sib.prj.current_project_index == 0


def test_current_project_details(sib):
    assert sib.prj.set_proj_as_default(index=1) is True
    sib.prj.init_default_proj()
    # sib.prj.print_current()
    cur_proj = sib.prj.current_project
    assert cur_proj.id == 2
    assert cur_proj.project_name == "Sample Proj 2"
    assert cur_proj.project_directory == "D:\\proj\\"
    assert cur_proj.working_directory == "fx\\"
    assert cur_proj.cameras_directory == "cam\\"
    assert cur_proj.cache_directory == "cache\\"
    assert cur_proj.env_directory == "env\\"
    assert cur_proj.props_directory == "props\\"
    assert cur_proj.scripts_directory == "scripts\\"
    assert cur_proj.custom_directory == "custom\\"

    assert cur_proj.working_directory_absolute == "D:\\proj\\fx\\"
    assert cur_proj.cameras_directory_absolute == "D:\\proj\\cam\\"
    assert cur_proj.cache_directory_absolute == "D:\\proj\\cache\\"
    assert cur_proj.env_directory_absolute == "D:\\proj\\env\\"
    assert cur_proj.props_directory_absolute == "D:\\proj\\props\\"
    assert cur_proj.scripts_directory_absolute == "D:\\proj\\scripts\\"
    assert cur_proj.custom_directory_absolute == "D:\\proj\\custom\\"

    assert cur_proj.is_default == 1
    assert cur_proj.state_id == 22
    assert cur_proj.state == "ACTIVE"
    assert cur_proj.description == "sample project 2"
    assert cur_proj.seq_shot_take_pattern == "<seq##>\\<sh###>"
    assert cur_proj.zeros_in_version == 3


def test_remove_single_project(sib):
    assert sib.prj.remove_single_project(id=1) is True
    assert sib.prj.total_projects == 2
    assert len(sib.prj.projects_data) == 2
    assert sib.prj.remove_single_project(index=1) is True
    assert sib.prj.total_projects == 1
    assert len(sib.prj.projects_data) == 1


def test_empty2_clear_all_projects_data(sib):
    assert sib.prj.clear_all_projects_data() is True
    assert sib.prj.total_projects == 0
    assert len(sib.prj.projects_data) == 0

def test_save_projects_to_json(sib):
    # assert sib.prj.save_projects_to_json() == True
    pass

# def test_get_dir_patterns(sib):   # TODO


def test_print_current(sib):
    sib.prj.print_current()


def test_print_all(sib):
    sib.prj.print_all()

