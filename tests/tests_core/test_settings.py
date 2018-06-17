
from simbatch.core import settings as sett
from simbatch.core.lib.common import Logger
import pytest
import os


@pytest.fixture(scope="module")
def settings():
    # TODO pytest-datadir pytest-datafiles
    settings_file = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep + "config_tests.ini"
    return sett.Settings(Logger(), 5, ini_file=settings_file)


def test_update_ui_colors(settings):
    settings.ui_color_mode = 1
    assert settings.update_ui_colors() is True


def test_check_data_integration(settings):
    assert settings.check_data_integration() is True


def test_print_all(settings):
    settings.print_all()
