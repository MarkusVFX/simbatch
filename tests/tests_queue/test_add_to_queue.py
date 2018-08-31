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

    assert sib.prj.total_projects > 0
    assert sib.sch.total_schemas > 0
    assert sib.tsk.total_tasks > 0
    assert sib.que.total_queue_items > 0


def test_get_evolutions_from_string(sib):
    evos = sib.pat.get_evolutions_from_string("BND 1 2 3")
    assert evos[0] == 3
    assert evos[1] == [['BND', '1.0', '2.0', '3.0']]

    evos = sib.pat.get_evolutions_from_string("BND 1 2 3; STR 4 5")
    assert evos[0] == 6
    assert evos[1][1] == ['STR', '4.0', '5.0']


def test_get_scripts_from_evolutions(sib):
    evos = sib.pat.get_evolutions_from_string("BND 1 2 3; STR 4 5")

    # sib.get_scripts_from_evolutions(evos)
    # sib.sch.current_schema
    #


def test_set_prj_sch_tsk(sib):
    assert sib.prj.max_id > 0
    sib.prj.update_current_from_id(sib.prj.max_id)
    assert sib.prj.current_project.id == sib.prj.max_id
    assert sib.prj.current_project_id == sib.prj.max_id

    sib.dfn.update_current_definition_by_name("Maya")
    sib.sch.update_current_from_id(sib.tsk.tasks_data[-1].schema_id)
    sib.tsk.update_current_from_id(sib.tsk.max_id)

    assert sib.sch.current_schema_id > 0
    assert sib.tsk.current_task_id > 0

    sib.que.remove_all_queue_items(only_done=True)

    # sib.que.print_all()
    assert sib.que.total_queue_items > 0
    # sib.que.print_queue_item(sib.que.queue_data[sib.que.total_queue_items-1])


def test_generate_template_queue_item(sib):
    print "\n\n___ template_queue_item ___"
    template_queue_item = sib.que.generate_template_queue_item(sib.tsk.current_task, sib.sch.current_schema)

    # script = sib.que.generate_script_from_Xactions(sib, sib.sch.current_schema)
    print " template_queue_item: ", template_queue_item
    # print " script: ", script
    # template_queue_item.evolution_script = script
    #template_queue_item.print_this()


def test_generate_queue_items(sib):
    print "\n\n___ queue_items ___"
    qi1 = sib.que.generate_queue_items(sib.tsk.current_task_id)
    for qi in qi1:
        print "___"
        qi.print_this()

def test_generate_queue_items(sib):
    print "\n\n___ queue_items ___"
    custom_action_inputs = ["ooppoo",[10, 99,"cape", "out","DMP 1 2 3"],"simed_file"]
    qi1 = sib.que.generate_queue_items(sib.tsk.current_task_id, action_inputs=custom_action_inputs)
    for qi in qi1:
        print "___"
        qi.print_this()


