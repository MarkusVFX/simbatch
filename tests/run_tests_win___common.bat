if not defined in_subprocess (cmd /k set in_subprocess=y ^& %0 %*) & exit )
pytest tests_core/test_common.py -vsx