# simbatch_no_gui_exampple

show_info = False

add_single = False
add_multi = False
add_param = True

clear_queue = True

import core.core as core

simbatch = core.SimBatch("no-gui", ini_file="config.ini")
simbatch.load_data()

if simbatch.prj.total_projects == 0:
    simbatch.create_example_data()

if simbatch.prj.current_project is None and simbatch.prj.total_projects > 0:
    simbatch.prj.update_current_from_id(simbatch.prj.max_id)

if show_info is True:
    simbatch.print_important_values()

# update def DFN SCH TSK
simbatch.dfn.update_current_definition_by_name("Maya")
simbatch.sch.update_current_from_id(simbatch.tsk.tasks_data[-1].schema_id)
simbatch.tsk.update_current_from_id(simbatch.tsk.max_id)

""" clear DONE queue items """
if clear_queue is True:
    simbatch.que.remove_all_queue_items(only_done=True)

""" add last task to queue """
if add_single is True:
    # new_queue_items = simbatch.tsk.generate_queue_items_from_task(simbatch.tsk.max_id)
    new_queue_items = simbatch.que.generate_queue_items(simbatch.tsk.max_id)
    # new_queue_items = simbatch.tsk.generate_queue_items_from_task(simbatch.tsk.max_id, evolutions=)
    # print new_queue_items
    simbatch.que.add_to_queue(new_queue_items)
    simbatch.que.save_queue()

""" add last task to queue with evolutions """
if add_multi is True:
    # evos_str = "Bnd 1 2; DMp 5 6 7"
    evos_str = "Bnd 111 222"
    ret = simbatch.pat.get_evolutions_from_string(evos_str)
    print "evos str 2 arr : ", ret
    # new_queue_items = simbatch.tsk.generate_queue_items_from_task(simbatch.tsk.max_id, evolutions=[evos_str])
    new_queue_items = simbatch.que.generate_queue_items(simbatch.tsk.max_id, evolutions=[evos_str])
    simbatch.que.add_to_queue(new_queue_items)
    simbatch.que.save_queue()

""" add last task to queue with evolutions and user params """
if add_param is True:
    evos_str = "Bnd 3 4"

    schema_options = simbatch.sch.create_schema_options_object()
    schema_options.set_action_value("Open", "open_file.mb")
    schema_options.set_action_value("Import", "<shot_cache_dir>/orc_*.xml")
    schema_options.set_action_value("Import", "<project_cache_dir>/captain_sword.xml")
    schema_options.set_action_value("Save", "custom_file_name_v<ver>.mb", occurrence=1)
    schema_options.set_action_value("Save", "<shot_dir>/backup/<schema_name>_<shot_name>__v<ver>.mb", occurrence=2)
    schema_options.set_action_value("Save", "<working_dir>/last_sim/last_sim.mb", occurrence=3)

    task_options = simbatch.tsk.create_task_options_object()
    task_options.set_task_value("sim_from", 10)
    task_options.set_task_value("sim_to", 40)
    task_options.set_task_value("prior", 22)
    task_options.set_task_value("user options", 22)

    """
    new_queue_items = simbatch.tsk.generate_queue_items_from_task(simbatch.tsk.max_id, evolutions=[evos_str],
                                                                  schema_options=schema_options,
                                                                  task_options=task_options)
    """

    new_queue_items = simbatch.que.generate_queue_items(simbatch.tsk.max_id, evolutions=[evos_str],
                                                        schema_options=schema_options, task_options=task_options)

    print "new q  : ", new_queue_items
    simbatch.que.add_to_queue(new_queue_items)
    simbatch.que.save_queue()


simbatch.que.print_header()
if simbatch.que.total_queue_items > 0:
    simbatch.que.print_queue_item(simbatch.que.queue_data[-1])


# print "___testy____"

"""
from core.io import PredefinedVariables

pre = PredefinedVariables(simbatch)
template = '"interactions.maya_render_blast(<ts> , <te> , "<f>"  )'
template = pre.convert_var_to_val("schema_base_setup", template)

print pre.convert_undefined_to_default(template)
"""

# print simbatch.tsk.proxy_task.id

