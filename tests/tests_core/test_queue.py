from simbatch.core import core as batch
import pytest


@pytest.fixture(scope="module")
def sib():
    # TODO pytest-datadir pytest-datafiles      vs       (   path.dirname( path.realpath(sys.argv[0]) )
    sib = batch.SimBatch(5, ini_file="S:/simbatch/tests/config_tests.ini")
    return sib

def test_prepare_data_directory_by_delete_all_files(sib):
    assert sib.s.store_data_mode is not None
    if sib.s.store_data_mode == 1:
        assert sib.comfun.path_exists(sib.s.store_data_json_directory) is True
    else:
        # PRO version with sql
        pass
    sib.q.clear_all_queue_items(clear_stored_data=True)

def test_no_queue_data(sib):
    assert len(sib.s.store_data_json_directory) > 0
    assert len(sib.s.JSON_SCHEMAS_FILE_NAME) > 0
    assert sib.comfun.file_exists(sib.s.store_data_json_directory + sib.s.JSON_QUEUE_FILE_NAME) is False

def test_create_example_queue_data(sib):
    assert sib.q.create_example_queue_data(do_save=True) == sib.q.sample_data_checksum
    # assert sib.sch.sample_data_checksum is not None
    # assert sib.sch.sample_data_total is not None
    # assert sib.sch.total_schemas == sib.sch.sample_data_total


def test_print_current(sib):
    sib.q.print_current()


def test_print_all(sib):
    sib.q.print_all()
