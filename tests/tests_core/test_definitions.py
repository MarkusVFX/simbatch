from simbatch.core import core
from simbatch.core.definitions import SingleAction
import pytest
import os


# TODO check dir on prepare tests
TESTING_AREA_DIR = "S:\\simbatch\\data\\"


@pytest.fixture(scope="module")
def simbatch():
    # TODO pytest-datadir pytest-datafiles      vs       (   path.dirname( path.realpath(sys.argv[0]) )
    settings_file = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep + "config_tests.ini"
    sib = core.SimBatch(5, ini_file=settings_file)
    sib.clear_all_memory_data()
    sib.prj.create_example_project_data(do_save=False)
    sib.prj.update_current_from_index(1)
    sib.sch.create_example_schemas_data(do_save=False)
    return sib


def test_exist_definitions_data(simbatch):
    assert simbatch.comfun.file_exists(simbatch.sts.store_definitions_directory_abs) is True


def test_load_definitions(simbatch):
    assert simbatch.dfn.load_definitions() is True

# def test_load_definitions(sib):
#     assert sib.dfn.load_definitions() is True


# def test_clear_all_definion_data


# def test_action_create(simbatch):
#     sa = SingleAction()
    # assert sa.
