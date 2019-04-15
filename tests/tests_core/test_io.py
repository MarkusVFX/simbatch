from simbatch.core import core
from simbatch.core import io as inout
from simbatch.core.lib import common
import pytest
import os


# TODO check dir on prepare tests
TESTING_AREA_DIR = "S:\\simbatch\\data\\"


@pytest.fixture(scope="module")
def io():
    # TODO pytest-datadir pytest-datafiles      vs       (   path.dirname( path.realpath(sys.argv[0]) )
    settings_file = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep + "config_tests.ini"
    sib = core.SimBatch("Stand-alone", ini_file=settings_file)
    sib.clear_all_memory_data()
    sib.prj.create_example_project_data(do_save=False)
    sib.prj.update_current_from_index(1)
    return sib.sio


def test_get_flat_name(io):
    assert io.get_flat_name("abc") == "abc"
    assert io.get_flat_name("ab c") == "ab_c"
    assert io.get_flat_name("a b c") == "a_b_c"
    assert io.get_flat_name("a b c ") == "a_b_c_"


def test_loaded_sample_project(io):
    assert io.batch.prj.total_projects == 3
    assert io.batch.prj.projects_data[1].project_name == "Sample Proj 2"


def test_generate_base_setup_file_name(io):
    base_setup = io.generate_base_setup_file_name(schema_name="test_schema")
    assert base_setup == "D:\\proj\\fx\\test_schema\\base_setup\\test_schema_v001.def"
