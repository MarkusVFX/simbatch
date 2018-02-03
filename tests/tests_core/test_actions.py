from simbatch.core import core
from simbatch.core.actions import SingleAction, GroupedActions
import pytest




# TODO check dir on prepare tests
TESTING_AREA_DIR = "S:\\simbatch\\data\\"


@pytest.fixture(scope="module")
def simbatch():
    # TODO pytest-datadir pytest-datafiles      vs       (   path.dirname( path.realpath(sys.argv[0]) )
    sib = core.SimBatch(5, ini_file="S:/simbatch/tests/config_tests.ini")
    sib.clear_all_memory_data()
    sib.prj.create_example_project_data(do_save=False)
    sib.prj.update_current_from_index(1)
    sib.sch.create_example_schemas_data(do_save=False)
    return sib



def test_single_action():
    sa = SingleAction(-1, "acti name", "descr", "abc", "template <f>")
    assert sa.name == "acti name"


def test_grouped_action():
    sia = SingleAction(-2, "acti name2", "descr2", "abc", "template2 <f>")
    gra = GroupedActions(1, "tst")
    assert gra.actions_count == 0
    gra.add_single_action(sia)
    assert gra.actions_count == 1



def test_exist_definitions_data(simbatch):
    assert simbatch.comfun.file_exists(simbatch.sts.store_definitions_directory) is True


def test_load_definitions(simbatch):
    assert simbatch.dfn.load_definitions() is True

# def test_load_definitions(sib):
#     assert sib.dfn.load_definitions() is True


# def test_action_create(simbatch):
#     sa = SingleAction()
    # assert sa.
