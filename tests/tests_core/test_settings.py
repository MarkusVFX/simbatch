
from simbatch.core import settings as sett
from simbatch.core.common import Logger
import pytest


@pytest.fixture(scope="module")
def settings():
    # TODO pytest-datadir pytest-datafiles
    return sett.Settings(Logger(), 5, ini_file="config_tests.ini")


def test_update_ui_colors(settings):
    settings.ui_color_mode = 1
    assert settings.update_ui_colors() is True


def test_check_data_integration(settings):
    assert settings.check_data_integration() is True


def test_print_all(settings):
    settings.print_all()
