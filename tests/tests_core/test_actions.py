from simbatch.core import core
from simbatch.core.actions import SingleAction, MultiAction
import pytest
import os


# TODO check dir on prepare tests
TESTING_AREA_DIR = "S:/simbatch/data/"


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


def test_single_action():
    sa = SingleAction("acti name", "descr", ["template ", "<f>"])
    assert sa.name == "acti name"
    assert sa.description == "descr"
    assert sa.template[0] == "template "
    assert sa.template[1] == "<f>"


def test_multi_action():
    singl_a1 = SingleAction("acti name1", "descr1", "template1 <f>")
    singl_a2 = SingleAction("acti name2", "descr2", "template2 <f>")
    multi_a = MultiAction(1, "tst")
    assert multi_a.actions_count == 0
    multi_a.add_single_action(singl_a1)
    assert multi_a.actions_count == 1
    multi_a.add_single_action(singl_a2)
    assert multi_a.actions_count == 2


def test_exist_definitions_data(simbatch):
    assert simbatch.comfun.file_exists(simbatch.sts.store_definitions_directory_abs) is True


def test_load_definitions(simbatch):
    assert simbatch.sts.store_definitions_directory_abs is not None
    assert len(simbatch.sts.store_definitions_directory_abs) > 0
    assert simbatch.dfn.load_definitions() is True

# def test_load_definitions(sib):
#     assert sib.dfn.load_definitions() is True


# def test_action_create(simbatch):
#     sa = SingleAction()
    # assert sa.
