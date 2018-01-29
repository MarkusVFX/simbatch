from simbatch.core import settings
from simbatch.core.common import Logger
import pytest


@pytest.fixture(scope="module")
def sett():
    # TODO pytest-datadir pytest-datafiles      vs       (   path.dirname( path.realpath(sys.argv[0]) )
    # return core.SimBatch(5, ini_file="S:/simbatch/tests/config_tests.ini")
    return settings.Settings(Logger(), 5, ini_file="S:/simbatch/tests/config_tests.ini")


def test_settings_file(sett):
    assert sett.comfun.file_exists(sett.ini_file) is True


def test_loading_state(sett):
    assert sett.loading_state == 3


def test_settings_data(sett):
    assert sett.json_settings_data is not None


def test_settings_mode(sett):
    sett.print_all()
    assert sett.store_data_mode is not None


def test_check_data_acces(sett):
    if sett.store_data_mode == 1:
        print "\n [INF] json dir:", sett.store_data_json_directory
        if sett.comfun.path_exists(sett.store_data_json_directory) is False:
            sett.comfun.create_directory(sett.store_data_json_directory)
        assert sett.comfun.path_exists(sett.store_data_json_directory) is True
    else:
        # PRO version with sql
        pass
