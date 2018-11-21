import os
import re
import pytest
from simbatch.core import settings
from simbatch.core.lib.common import Logger


@pytest.fixture(scope="module")
def sett():
    #return settings.Settings(Logger(), 5)
    return settings.Settings(Logger(), 5, ini_path="tests")


def test_get_ini_file_and_path(sett):
    if sett.current_os == 1:  # linux
        assert re.match(r'^.*/(?!.*/)(.*)$', sett.get_ini_file_and_path())
    if sett.current_os == 2:  # win
        assert re.match(r'[a-zA-Z]:\\((?:[a-zA-Z0-9() ]*\\)*).*', sett.get_ini_file_and_path())
        # TODO  add network path for regex:   //srv/storage/sib/config.ini


def test_empty_get_ini_file_and_path(sett):
    if sett.current_os == 1:   # linux
        assert re.match(r'^.*/(?!.*/)(.*)$', sett.get_ini_file_and_path("", ""))
    if sett.current_os == 2:   # win
        assert re.match(r'[a-zA-Z]:\\((?:[a-zA-Z0-9() ]*\\)*).*', sett.get_ini_file_and_path("", ""))
        # TODO  add network path for regex:   //srv/storage/sib/config.ini


def test_absolute_get_ini_file_and_path(sett):
    assert sett.get_ini_file_and_path(ini_file="s:\\test.ini", check_is_exists=False) == "s:\\test.ini"


def test_params_get_ini_file_and_path(sett):
    print "sett.ini_file: ", sett.ini_file
    assert sett.get_ini_file_and_path("s:\\", "test.ini", check_is_exists=False) == "s:\\test.ini"
    assert sett.get_ini_file_and_path(ini_path="s:\\", check_is_exists=False) == "s:\\config.ini"
    assert sett.get_ini_file_and_path(ini_path="s:\\sib\\", ini_file="test.ini", check_is_exists=False) == "s:\\sib\\test.ini"
    assert sett.get_ini_file_and_path("s:\\", check_is_exists=False) == "s:\\config.ini"
    assert sett.get_ini_file_and_path("//srv/storage/", "conf.ini", check_is_exists=False) == "//srv/storage/conf.ini"
    assert sett.get_ini_file_and_path("/srv/", "", check_is_exists=False) == "/srv/config.ini"
    assert sett.get_ini_file_and_path("/srv/", "custom_config.ini", check_is_exists=False) == "/srv/custom_config.ini"


def test_options_get_ini_file_and_path(sett):
    tests_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + sett.dir_separator
    tests_dir = tests_dir + "tests" + sett.dir_separator
    assert sett.get_ini_file_and_path(ini_path="tests", check_is_exists=False) == tests_dir + "config_tests.ini"
    custom_tests_config_file = sett.get_ini_file_and_path(ini_path="tests", ini_file="testing.dat", check_is_exists=False)
    assert custom_tests_config_file == tests_dir + "testing.dat"


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

