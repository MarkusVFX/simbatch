from simbatch.core import common
import pytest


@pytest.fixture
def comfun():
    return common.CommonFunctions(5)


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


def test_int_or_val(comfun):
    assert comfun.int_or_val(1, 5) == 1
    assert comfun.int_or_val("1", 5) == 1
    assert comfun.int_or_val("z", 5) == 5


def test_str_with_zeros(comfun):
    assert comfun.str_with_zeros("1") == "001"
    assert comfun.str_with_zeros(20) == "020"
    assert comfun.str_with_zeros("4000") == "4000"
    assert comfun.str_with_zeros(4000, zeros=5) == "04000"


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


def test_std_is_absolute(comfun):
    assert comfun.is_absolute("c:\\\\dir\\\\win") is True
    assert comfun.is_absolute("c:/dir/win") is True
    assert comfun.is_absolute("\\\\serv\\dir") is True


def test_std_get_incremented_name(comfun):
    assert comfun.get_incremented_name("name_no_123_number", db=True) == "name_no_123_number_02"
    assert comfun.get_incremented_name("name__123") == "name__124"
    assert comfun.get_incremented_name("name__1") == "name__2"
    assert comfun.get_incremented_name("name__4", db=True) == "name__5"

