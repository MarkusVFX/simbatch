# import sys
# from os import path
from simbatch.core import core as b
from simbatch.core import projects
import pytest
from simbatch.core.common import CommonFunctions


@pytest.fixture(scope="module")
def proj():
    # print "\n  [tst] config.ini " ,  (   path.dirname( path.realpath(sys.argv[0]) ) +"\\" )
    # TODO pytest-datadir pytest-datafiles
    batch = b.SimBatch(5, ini_file="S:/simbatch/simbatch/config.ini")
    return projects.Projects(batch)


def test_get_index_from_id(proj):
    assert proj.get_index_from_id(2) is None


def test_empty1_clear_all_projects_data(proj):
    assert proj.clear_all_projects_data() is True


def test_create_example_project_data(proj):
    assert proj.create_example_project_data(do_save=False) == 6
    assert proj.total_projects == 3


def test_get2_index_from_id(proj):
    assert proj.get_index_from_id(2) == 1


def test_total_projects(proj):
    assert proj.total_projects == 3
    assert len(proj.projects_data) == 3


def test_update_current_from_id(proj):
    assert proj.current_project_id is None
    assert proj.current_project_index is None
    assert proj.update_current_from_id(2) is True
    # proj.print_all()
    assert proj.current_project_id == 2
    assert proj.current_project_index == 1


def test_update_current_from_index(proj):
    proj.current_project_id = None
    proj.current_project_index = None
    assert proj.update_current_from_index(2) is True
    assert proj.current_project_id == 3
    assert proj.current_project_index == 2


def test_check_is_default(proj):
    assert proj.check_is_default(index=1) is False
    assert proj.check_is_default(index=2) is True


def test_by_id_set_proj_as_default(proj):
    assert proj.set_proj_as_default(id=1) is True
    index = proj.get_index_from_id(1)
    assert proj.check_is_default(index=index) is True
    assert proj.set_proj_as_default(id=2) is True
    index = proj.get_index_from_id(2)
    assert proj.check_is_default(index=index) is True


def test_by_index_set_proj_as_default(proj):
    assert proj.set_proj_as_default(index=0) is True
    assert proj.check_is_default(index=0) is True
    assert proj.set_proj_as_default(index=1) is True
    assert proj.check_is_default(index=1) is True


def test_init_default_proj(proj):
    assert proj.current_project_id == 3
    assert proj.current_project_index == 2
    proj.init_default_proj()
    assert proj.current_project_id == 2
    assert proj.current_project_index == 1


def test_remove_single_project(proj):
    assert proj.remove_single_project(id=1) is True
    assert proj.total_projects == 2
    assert len(proj.projects_data) == 2
    assert proj.remove_single_project(index=1) is True
    assert proj.total_projects == 1
    assert len(proj.projects_data) == 1


def test_empty2_clear_all_projects_data(proj):
    assert proj.clear_all_projects_data() is True
    assert proj.total_projects == 0
    assert len(proj.projects_data) == 0


def test_load_projects_from_json(proj):
    comfun = CommonFunctions()
    file = "S:/simbatch/data/data_projects.json"  #  TODO rel path
    json_projects = comfun.load_json_file(file)
    jskon_keys = json_projects.keys()
    assert ("projects" in jskon_keys) is True
    assert proj.load_projects_from_json() is True
    #load_projects_from_json
    1

def test_save_projects_to_json(proj):
    #assert proj.save_projects_to_json() == True
    1
'''

def test_get_dir_patterns(proj): # TODO
    assert proj.get_index_from_id(2) == 1

'''
