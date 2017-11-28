from simbatch.core import core
from simbatch.core import settings
import pytest


@pytest.fixture(scope="module")
def sib():
    # TODO pytest-datadir pytest-datafiles
    ini_file = "S:/simbatch/simbatch/config.ini"
    return core.SimBatch(5, ini_file="S:/simbatch/simbatch/config.ini")


def test_init_simbatch(sib):
    assert sib.s.soft_id == 5
    assert sib.p.total_projects == 0
    assert sib.c.total_schemas == 0
    assert sib.t.total_tasks == 0
    assert sib.q.total_queue_jobs == 0
    assert sib.n.total_nodes == 0

def test_load_data(sib):
    assert sib.load_data() == True

def test_check_loaded_data(sib):
    assert sib.p.total_projects > 0
    assert sib.p.total_projects == len(sib.p.projects_data)