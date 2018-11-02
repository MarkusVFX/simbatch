import os
import pytest
from simbatch.core import settings
from simbatch.core.lib.common import Logger


@pytest.fixture(scope="module")
def sett():
    # TODO pytest-datadir pytest-datafiles      vs       (   path.dirname( path.realpath(sys.argv[0]) )
    settings_file = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep + "config_tests.ini"
    return settings.Settings(Logger(), 5, ini_file=settings_file)


def test_settings_file(sett):
    print "\n [db] config ini file :", sett.ini_file
    assert sett.comfun.file_exists(sett.ini_file) is True


def test_data_json_directory_abs(sett):
    print "\n [db] store_data_json_directory_abs :", sett.store_data_json_directory_abs
    assert sett.comfun.path_exists(sett.store_data_json_directory_abs) is True


def test_definitions_directory_abs(sett):
    print "\n [db] store_definitions_directory_abs :", sett.store_definitions_directory_abs
    assert sett.comfun.path_exists(sett.store_definitions_directory_abs) is True


def test_loading_state(sett):
    assert sett.loading_state == 4


def test_settings_data(sett):
    assert sett.json_settings_data is not None


def test_settings_mode(sett):
    sett.print_all()
    assert sett.store_data_mode is not None


def test_check_data_access(sett):
    if sett.store_data_mode == 1:
        print "\n [INF] json dir:", sett.store_data_json_directory_abs
        if sett.comfun.path_exists(sett.store_data_json_directory_abs) is False:
            sett.comfun.create_directory(sett.store_data_json_directory_abs)
        assert sett.comfun.path_exists(sett.store_data_json_directory_abs) is True
    else:
        # PRO version with sql
        pass

def test_is_data_exist(sett, capsys):
    if sett.store_data_mode == 1:
        assert sett.JSON_PROJECTS_FILE_NAME is not None
        prj_file = sett.store_data_json_directory_abs + sett.JSON_PROJECTS_FILE_NAME
        if sett.comfun.file_exists(prj_file) is False:
            with capsys.disabled():
                print "\n[pytest WRN] Projects data file not exist: ", prj_file
        assert sett.JSON_SCHEMAS_FILE_NAME is not None
        sch_file = sett.store_data_json_directory_abs + sett.JSON_SCHEMAS_FILE_NAME
        if sett.comfun.file_exists(sch_file) is False:
            with capsys.disabled():
                print "\n[pytest WRN] Schemas data file not exist: ", sch_file
        assert sett.JSON_TASKS_FILE_NAME is not None
        tsk_file = sett.store_data_json_directory_abs + sett.JSON_TASKS_FILE_NAME
        if sett.comfun.file_exists(tsk_file) is False:
            with capsys.disabled():
                print "\n[pytest WRN] Tasks data file not exist: ", tsk_file
        assert sett.JSON_QUEUE_FILE_NAME is not None
        que_file = sett.store_data_json_directory_abs + sett.JSON_QUEUE_FILE_NAME
        if sett.comfun.file_exists(que_file) is False:
            with capsys.disabled():
                print "\n[pytest WRN] Queue data file not exist: ", que_file
        assert sett.JSON_SIMNODES_FILE_NAME is not None
        nod_file = sett.store_data_json_directory_abs + sett.JSON_SIMNODES_FILE_NAME
        if sett.comfun.file_exists(nod_file) is False:
            with capsys.disabled():
                print "\n[pytest WRN] Project data file not exist: ", nod_file
    else:
        # PRO version with sql
        pass

