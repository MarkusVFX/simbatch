from simbatch.core import core
from simbatch.core import settings
import pytest
import os


@pytest.fixture(scope="module")
def sib():
    # TODO pytest-datadir pytest-datafiles      vs       (   path.dirname( path.realpath(sys.argv[0]) )
    settings_file = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + os.sep + "config_tests.ini"
    return core.SimBatch("Stand-alone", ini_file=settings_file)


def test_init_simbatch(sib):
    #
    sib.sts.debug_level = 0
    sib.logger.console_level = 0
    #
    assert sib.sts.runtime_env == "Stand-alone"
    lo = sib.load_data()
    assert lo[0] is True


def test_set_prj_sch_tsk(sib):
    sib.sio.create_unit_tests_example_data(do_save=True)
    utest_proj_id = sib.prj.get_id_from_name("pytest proj")
    assert utest_proj_id is not None
    assert sib.prj.update_current_from_id(sib.prj.max_id) is True
    assert sib.prj.current_project.project_name == "pytest proj"

    sib.dfn.update_current_definition_by_name("Maya")
    sib.sch.update_current_from_id(sib.tsk.tasks_data[-1].schema_id)
    sib.tsk.update_current_from_id(sib.tsk.max_id)

    assert sib.tsk.current_task_id > 0

    sib.que.remove_queue_items(only_done=True)


def test_generate_template_queue_item(sib):
    print "\n\n___ template_queue_item ___"
    template_queue_item = sib.que.generate_template_queue_item(sib.tsk.current_task, sib.sch.current_schema)
    assert template_queue_item.shot == "ut01"
    template_queue_item.print_this()


def test_generate_template_evo_script(sib):
    print "\n\n___ template script ___"
    for i, act in enumerate(sib.sch.current_schema.actions_array):
        act.actual_value = "test_user_input_" + str(i+1)
    template_script = sib.que.generate_template_evo_script(sib.sch.current_schema)
    print template_script


def test_get_params_val_arr_from_string(sib):
    evos_var = sib.pat.get_params_val_arr_from_string("BND 1 2 3")
    assert evos_var[0] == 3
    assert evos_var[1] == [['BND', '1.0', '2.0', '3.0']]

    evos_var = sib.pat.get_params_val_arr_from_string("bNd 7 14.5; stR 4.00 5 6")
    assert evos_var[0] == 6
    assert evos_var[1][0] == ['BND', '7.0', '14.5']
    assert evos_var[1][1] == ['STR', '4.0', '5.0', '6.0']

    evos_var = sib.pat.get_params_val_arr_from_string("bNd  7 7 14.5 7 14.5; stR 4.00 5 6  ; MASS  123 4 5; MAS 1 2 3")
    assert evos_var[0] == 18
    assert evos_var[1][0] == ['BND', '7.0', '14.5']
    assert evos_var[1][1] == ['STR', '4.0', '5.0', '6.0']
    assert evos_var[1][2] == ['MAS', '1.0', '2.0', '3.0']

    # TODO
    # evos_var = sib.pat.get_params_val_arr_from_string("stR 4.00 5 6  ; ZZZ  123 4 5; MAS 1 2 3")
    # evos_var = sib.pat.get_params_val_arr_from_string("stR 4.00 5 6  ; ZZZZZ  123 4 5  MAS 1 2 3")


def test_get_array_of_scripts_params_val_from_schema_actions(sib):
    print "\n\n___ scripts_params ___"
    arr_scripts_params = sib.que.get_array_of_scripts_params_val_from_schema_actions(sib.sch.current_schema)
    print "\n", arr_scripts_params

    evo_action_index = sib.sch.current_schema.get_first_evos_possible()
    if evo_action_index is not None:
        sib.sch.current_schema.actions_array[evo_action_index].actual_value = "Bnd 5 55"
    arr_scripts_params = sib.que.get_array_of_scripts_params_val_from_schema_actions(sib.sch.current_schema)
    print "\n", arr_scripts_params

    evo_action_index = sib.sch.current_schema.get_first_evos_possible()
    if evo_action_index is not None:
        sib.sch.current_schema.actions_array[evo_action_index].actual_value = "bND 5 55; MAS 1 2 3"
    arr_scripts_params = sib.que.get_array_of_scripts_params_val_from_schema_actions(sib.sch.current_schema)
    print "\n", arr_scripts_params

    evo_action_index = sib.sch.current_schema.get_first_evos_possible()
    if evo_action_index is not None:
        sib.sch.current_schema.actions_array[evo_action_index].actual_value = "bND 5 55; MAS 1 2 3; STI 300 303"
    arr_scripts_params = sib.que.get_array_of_scripts_params_val_from_schema_actions(sib.sch.current_schema)
    print "\n", arr_scripts_params


def test_do_params_combinations(sib):
    print "\n\n___ params_combinations ___"
    arr_scripts_params = sib.que.get_array_of_scripts_params_val_from_schema_actions(sib.sch.current_schema)
    all_evo_combinations_array = sib.que.do_params_combinations(arr_scripts_params)
    print "\n", all_evo_combinations_array

    in_arr = [[[u'STR:7.0', u'i'], [u'STR:8.0', u'i']]]
    assert len(sib.que.do_params_combinations(in_arr)) == 2   # TODO check value !!!
    in_arr = [[[u'STR:7.0', u'i'], [u'STR:8.0', u'i']],[[u'LFT:1.0', u'i'], [u'LFT:2.0', u'i']]]
    assert len(sib.que.do_params_combinations(in_arr)) == 4   # TODO check value !!!


def test_generate_queue_items(sib):
    print "\n\n___ queue_items ___"
    qi1 = sib.que.generate_queue_items(sib.tsk.current_task_id)
    # for qi in qi1:
    #     print "___"
    #     qi.print_this()
    # WIP


def test_generate_queue_items_evo(sib):
    print "\n\n___ queue_items with evo ___"
    assert len(sib.tsk.tasks_data) > 0
    sib.sch.update_current_from_id(sib.tsk.tasks_data[-1].schema_id)
    sib.tsk.update_current_from_id(sib.tsk.max_id)
    # sib.print_important_values()

    custom_action_inputs = [["ooppoo"], [["sim_clt"], "DMP 1 2 3"], ["simed_file"]]
    # TO DO !!! , action_inputs = custom_action_inputs
    qi1 = sib.que.generate_queue_items(sib.tsk.current_task_id)
    # for qi in qi1:
    #     print "___"
    #     qi.print_this()
    # WIP

