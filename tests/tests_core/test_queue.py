from simbatch.core import core as batch
import pytest
import os


@pytest.fixture(scope="module")
def sib():
    # TODO pytest-datadir pytest-datafiles      vs       (   path.dirname( path.realpath(sys.argv[0]) )
    settings_file = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep + "config_tests.ini"
    sib = batch.SimBatch(5, ini_file=settings_file)
    return sib


def test_prepare_data_directory_by_delete_all_files(sib):
    assert sib.sts.store_data_mode is not None
    if sib.sts.store_data_mode == 1:
        assert sib.comfun.path_exists(sib.sts.store_data_json_directory_abs) is True
    else:
        # PRO version with sql
        pass
    sib.que.clear_all_queue_items(clear_stored_data=True)
    sib.que.delete_json_queue_file()


def test_no_queue_data(sib):
    assert len(sib.sts.store_data_json_directory_abs) > 0
    assert len(sib.sts.JSON_SCHEMAS_FILE_NAME) > 0
    assert sib.comfun.file_exists(sib.sts.store_data_json_directory_abs + sib.sts.JSON_QUEUE_FILE_NAME) is False


def test_create_example_queue_data(sib):
    assert sib.que.create_example_queue_data(do_save=True) == sib.que.sample_data_checksum
    # assert sib.sch.sample_data_checksum is not None
    # assert sib.sch.sample_data_total is not None
    # assert sib.sch.total_schemas == sib.sch.sample_data_total


def test_print_current(sib):
    sib.que.print_current()


def test_print_all(sib):
    sib.que.print_all()
