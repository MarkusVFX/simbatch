from random import randint
from os import path, sep
from shutil import rmtree
from time import sleep
from simbatch.core.lib import common
import pytest


# TODO check dir on prepare tests
TESTING_AREA_DIR = path.dirname(path.dirname(path.abspath(__file__))) + sep
TEST_DIR = "test_dir/"
random_file = None


@pytest.fixture
def comfun():
    return common.CommonFunctions()


def test_prepare_env(comfun):
    if path.exists(TESTING_AREA_DIR+TEST_DIR) is True:  # clear TESTING_AREA_DIR
        print "\n\n [test db] dir exists:", TESTING_AREA_DIR+TEST_DIR
        rmtree(TESTING_AREA_DIR+TEST_DIR, ignore_errors=True)
        sleep(5) # case TEST_DIR is user's current directory


def test_std_list_as_string(comfun):
    assert comfun.list_as_string(["a", "b", "c"]) == "a;b;c"


def test_dot_list_as_string(comfun):
    assert comfun.list_as_string(["a", "b", "c"], separator=".") == "a.b.c"


def test_first_list_as_string(comfun):
    assert comfun.list_as_string(["a", "b", "c"], only_first=True) == "a"


def test_single_list_as_string(comfun):
    assert comfun.list_as_string(["a"]) == "a"


def test_single_string_as_list(comfun):
    assert comfun.string_as_list("a") == ["a"]


def test_std_string_as_list(comfun):
    assert comfun.string_as_list("a;b;cde;fgh") == ["a", "b", "cde", "fgh"]


def test_separator_string_as_list(comfun):
    assert comfun.string_as_list("a.b.cde.fgh", separator=".") == ["a", "b", "cde", "fgh"]


def test_empty_string_as_list(comfun):
    assert comfun.string_as_list("a.b..cde.fgh", remove_empty=False, separator=".") == ["a", "b", "", "cde", "fgh"]


def test_remove2_string_as_list(comfun):
    assert comfun.string_as_list("a;bb;cde;fghh", remove_shorter_than=2) == ["bb", "cde", "fghh"]


def test_remove3_string_as_list(comfun):
    assert comfun.string_as_list("a;bb;;;;cde;fghh", remove_empty=True, remove_shorter_than=3) == ["cde", "fghh"]


def test_can_get_int(comfun):
    assert comfun.can_get_int("a") is False
    assert comfun.can_get_int('abc') is False
    assert comfun.can_get_int(None) is False


def test_int_or_val(comfun):
    assert comfun.int_or_val(1, 5) == 1
    assert comfun.int_or_val("1", 5) == 1
    assert comfun.int_or_val("z", 5) == 5


def test_str_with_zeros(comfun):
    assert comfun.str_with_zeros("1") == "001"
    assert comfun.str_with_zeros(20) == "020"
    assert comfun.str_with_zeros("4000") == "4000"
    assert comfun.str_with_zeros(4000, zeros=5) == "04000"


def test_str_with_spaces(comfun):
    assert comfun.str_with_spaces("ok") == "ok "
    assert comfun.str_with_spaces("ok", length=5) == "ok   "
    assert comfun.str_with_spaces("oki", length=5, as_prefix=True) == "  oki"
    assert comfun.str_with_spaces("___oki", length=5, as_prefix=True) == "___oki"
    assert comfun.str_with_spaces("___oki") == "___oki"
    assert comfun.str_with_spaces("___oki___") == "___oki___"


def test_std_find_string_in_list(comfun):
    assert comfun.find_string_in_list(["aaa", "bbb", "abc", "abcde", "cde"], "ab") is None


def test_exactly_find_string_in_list(comfun):
    assert comfun.find_string_in_list(["aaa", "bbb", "abc", "abcde", "cde"], "ab", exactly=False) == 2


def test_starting_find_string_in_list(comfun):
    assert comfun.find_string_in_list(["zabc", "abcde", "cde"], "ab", starting=True) is None


def test_starting_exacly_find_string_in_list(comfun):
    assert comfun.find_string_in_list(["zabc", "abcde", "cde"], "ab", starting=True, exactly=False) == 1


def test_seconds_format_seconds_to_string(comfun):
    assert comfun.format_seconds_to_string(1) == "1s"
    assert comfun.format_seconds_to_string(40) == "40s"


def test_minutes_format_seconds_to_string(comfun):
    assert comfun.format_seconds_to_string(60) == "1.0m"
    assert comfun.format_seconds_to_string(80) == "1.3m"
    assert comfun.format_seconds_to_string(220) == "3.7m"
    assert comfun.format_seconds_to_string(750) == "12.5m"


def test_hours_format_seconds_to_string(comfun):
    assert comfun.format_seconds_to_string(6500) == "1.8h"
    assert comfun.format_seconds_to_string(7500) == "2.1h"
    assert comfun.format_seconds_to_string(75000) == "20.8h"


def test_get_proper_path_01(comfun):
    assert comfun.get_proper_path("aaaa") == "aaaa\\"


def test_get_proper_path_02(comfun):
    assert comfun.get_proper_path("c:/cee") == "c:/cee/"


def test_get_proper_path_03(comfun):
    assert comfun.get_proper_path("\\\\proj\\cee") == "\\\\proj\\cee\\"


def test_get_proper_path_04(comfun):
    assert comfun.get_proper_path("path\\") == "path\\"


def test_get_proper_path_05(comfun):
    assert comfun.get_proper_path("path/") == "path/"


def test_get_path_from_full(comfun):
    assert comfun.get_path_from_full("c:\\oki\\doki\\test.png") == "c:\\oki\\doki\\"
    assert comfun.get_path_from_full("\\\\serv\\doki\\test.png") == "\\\\serv\\doki\\"


def test_create_directory(comfun):
    print "TESTING_AREA_DIR: ", TESTING_AREA_DIR
    assert comfun.path_exists(TESTING_AREA_DIR) is True
    assert comfun.path_exists(TESTING_AREA_DIR + TEST_DIR) is False
    assert comfun.create_directory(TESTING_AREA_DIR + TEST_DIR) is True
    assert comfun.path_exists(TESTING_AREA_DIR + TEST_DIR) is True


def test_wrong_file_param(comfun):
    assert comfun.file_exists("") is False


def test_not_file_exists(comfun):
    global random_file
    random_str = str(randint(1000, 9999))
    random_file = "{}test_dir/random_file_{}.txt".format(TESTING_AREA_DIR, random_str)
    assert comfun.file_exists(random_file) is False


def test_create_empty_file(comfun):
    assert comfun.create_empty_file(random_file) is True


def test_file_exists(comfun):
    assert comfun.file_exists(random_file) is True


def test_delete_file(comfun):
    assert comfun.delete_file(random_file) is True


def test_remove_directory(comfun):
    assert comfun.path_exists(TESTING_AREA_DIR) is True
    assert comfun.path_exists(TESTING_AREA_DIR + "test_dir") is True
    assert comfun.remove_directory(TESTING_AREA_DIR + "test_dir") is True
    assert comfun.path_exists(TESTING_AREA_DIR + "test_dir") is False


def test_std_is_absolute(comfun):
    assert comfun.is_absolute("c:\\\\dir\\\\win") is True
    assert comfun.is_absolute("c:/dir/win") is True
    assert comfun.is_absolute("\\\\serv\\dir") is True


def test_std_get_incremented_name(comfun):
    assert comfun.get_incremented_name("name_no_123_number", db=True) == "name_no_123_number_02"
    assert comfun.get_incremented_name("name__123") == "name__124"
    assert comfun.get_incremented_name("name__1") == "name__2"
    assert comfun.get_incremented_name("name__4", db=True) == "name__5"
