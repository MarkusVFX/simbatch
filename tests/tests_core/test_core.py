from simbatch.core import core
from simbatch.core import settings
import pytest


@pytest.fixture(scope="module")
def sib():
    # TODO pytest-datadir pytest-datafiles      vs       (   path.dirname( path.realpath(sys.argv[0]) )
    return core.SimBatch(5, ini_file="S:/simbatch/tests/config_tests.ini")


def test_init_simbatch(sib):
    assert sib.s.soft_id == 5
    assert sib.p.total_projects == 0
    assert sib.c.total_schemas == 0
    assert sib.t.total_tasks == 0
    assert sib.q.total_queue_items == 0
    assert sib.n.total_nodes == 0


def test_clear_all_memory_data(sib):
    sib.clear_all_memory_data()
    assert sib.p.total_projects == 0
    assert len(sib.p.projects_data) == 0
    assert sib.c.total_schemas == 0
    assert len(sib.c.schemas_data) == 0


def test_sample_projects(sib):
    assert sib.p.create_example_project_data(do_save=False) == sib.p.sample_data_checksum
    assert sib.p.sample_data_checksum is not None
    assert sib.p.sample_data_total is not None
    assert sib.p.total_projects == sib.p.sample_data_total

def test_sample_schemas(sib):
    assert sib.c.create_example_schemas_data(do_save=False) == sib.c.sample_data_checksum
    assert sib.c.sample_data_checksum is not None
    assert sib.c.sample_data_total is not None
    assert sib.c.total_schemas == sib.c.sample_data_total


def test_sample_tasks(sib):
    assert sib.t.create_example_tasks_data(do_save=False) == sib.t.sample_data_checksum
    assert sib.t.sample_data_checksum is not None
    assert sib.t.sample_data_total is not None
    assert sib.t.total_tasks == sib.t.sample_data_total

def test_check_loaded_data(sib):
    assert sib.p.total_projects > 0
    assert sib.p.total_projects == len(sib.p.projects_data)

    assert sib.c.total_schemas > 0
    assert sib.c.total_schemas == len(sib.c.schemas_data)

    assert sib.t.total_tasks > 0
    assert sib.t.total_tasks == len(sib.t.tasks_data)

def test_load_data(sib):
    assert sib.load_data() is True
