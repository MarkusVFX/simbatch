from simbatch.core import core
from simbatch.core import io as inout
from simbatch.core import common
import pytest

# TODO check dir on prepare tests
TESTING_AREA_DIR = "S:\\simbatch\\data\\"


@pytest.fixture(scope="module")
def io():
    # TODO pytest-datadir pytest-datafiles      vs       (   path.dirname( path.realpath(sys.argv[0]) )
    sib = core.SimBatch("Stand-alone", ini_file="S:/simbatch/tests/config_tests.ini")
    sib.clear_all_memory_data()
    sib.prj.create_example_project_data(do_save=False)
    sib.prj.update_current_from_index(1)
    return sib.i


def test_get_flat_name(io):
    assert io.get_flat_name("abc") == "abc"
    assert io.get_flat_name("ab c") == "ab_c"
    assert io.get_flat_name("a b c") == "a_b_c"


def test_loaded_sample_project(io):
    assert io.batch.prj.total_projects == 3
    assert io.batch.prj.projects_data[1].project_name == "Sample Proj 2"


def test_generate_base_setup_file_name(io):
    tuple_base_setup = io.generate_base_setup_file_name(schema_name="test_schema")
    assert  tuple_base_setup[0] == 1
    # assert  tuple_base_setup[1] == "D:\\proj\\fx\\test_schema\\base_setup\\test_schema_v001.null"
    # TODO12
