from simbatch.core import core
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


def test_exist_definitions_data(simbatch):
    assert simbatch.comfun.file_exists(simbatch.s.store_definitions_directory) is True


def test_load_definitions(simbatch):
    assert simbatch.dfn.load_definitions() is True

# def test_load_definitions(sib):
#     assert sib.dfn.load_definitions() is True
