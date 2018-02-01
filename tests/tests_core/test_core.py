from simbatch.core import core
from simbatch.core import settings
import pytest


@pytest.fixture(scope="module")
def sib():
    # TODO pytest-datadir pytest-datafiles      vs       (   path.dirname( path.realpath(sys.argv[0]) )
    return core.SimBatch("Stand-alone", ini_file="S:/simbatch/tests/config_tests.ini")


def test_init_simbatch(sib):
    assert sib.s.runtime_env == "Stand-alone"
    assert sib.prj.total_projects == 0
    assert sib.sch.total_schemas == 0
    assert sib.tsk.total_tasks == 0
    assert sib.que.total_queue_items == 0
    assert sib.n.total_nodes == 0


def test_clear_all_memory_data(sib):
    sib.clear_all_memory_data()
    assert sib.prj.total_projects == 0
    assert len(sib.prj.projects_data) == 0
    assert sib.sch.total_schemas == 0
    assert len(sib.sch.schemas_data) == 0


def test_sample_projects(sib):
    assert sib.prj.create_example_project_data(do_save=False) == sib.prj.sample_data_checksum
    assert sib.prj.sample_data_checksum is not None
    assert sib.prj.sample_data_total is not None
    assert sib.prj.total_projects == sib.prj.sample_data_total

def test_sample_schemas(sib):
    assert sib.sch.create_example_schemas_data(do_save=False) == sib.sch.sample_data_checksum
    assert sib.sch.sample_data_checksum is not None
    assert sib.sch.sample_data_total is not None
    assert sib.sch.total_schemas == sib.sch.sample_data_total


def test_sample_tasks(sib):
    assert sib.tsk.create_example_tasks_data(do_save=False) == sib.tsk.sample_data_checksum
    assert sib.tsk.sample_data_checksum is not None
    assert sib.tsk.sample_data_total is not None
    assert sib.tsk.total_tasks == sib.tsk.sample_data_total

def test_check_loaded_data(sib):
    assert sib.prj.total_projects > 0
    assert sib.prj.total_projects == len(sib.prj.projects_data)

    assert sib.sch.total_schemas > 0
    assert sib.sch.total_schemas == len(sib.sch.schemas_data)

    assert sib.tsk.total_tasks > 0
    assert sib.tsk.total_tasks == len(sib.tsk.tasks_data)

def test_load_data(sib):
    assert sib.load_data() is True
