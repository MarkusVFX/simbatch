from simbatch.core import core
import pytest




# TODO check dir on prepare tests
TESTING_AREA_DIR = "S:\\simbatch\\data\\"


@pytest.fixture(scope="module")
def sib():
    # TODO pytest-datadir pytest-datafiles      vs       (   path.dirname( path.realpath(sys.argv[0]) )
    sib = core.SimBatch(5, ini_file="S:/simbatch/tests/config_tests.ini")
    sib.clear_all_memory_data()
    sib.p.create_example_project_data(do_save=False)
    sib.p.update_current_from_index(1)
    sib.c.create_example_schemas_data(do_save=False)
    return sib



def test_exist_definitions_data(sib):
    assert sib.comfun.file_exists(sib.s.store_data_definitions_directory) is True


def test_load_definitions(sib):
    assert sib.d.load_definitions() is True