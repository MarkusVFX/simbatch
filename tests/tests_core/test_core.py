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
    assert sib.q.total_queue_jobs == 0
    assert sib.n.total_nodes == 0


def test_clear_all_memory_data(sib):
    sib.clear_all_memory_data()
    assert sib.p.total_projects == 0
    assert len(sib.p.projects_data) == 0
    assert sib.c.total_schemas == 0
    assert len(sib.c.schemas_data) == 0


def test_load_projects(sib):
    assert sib.p.load_projects() is True


def test_load_data(sib):
    assert sib.load_data() is True


def test_check_loaded_data(sib):
    assert sib.p.total_projects > 0
    assert sib.p.total_projects == len(sib.p.projects_data)
