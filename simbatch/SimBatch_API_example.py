# simbatch_no_gui_exampple

show_info = False

add_single = False
add_multi = False
add_param = True

clear_queue = True

#
##
###
#####
########
################
########################

import core.core as core

""" init SimBATCH """
simbatch = core.SimBatch("no-gui", ini_file="config.ini")
simbatch.load_data()

""" show data source """
if show_info is True:
    print "data dir: ", simbatch.sts.store_data_json_directory_abs
    print "settings data: ", simbatch.sts.json_settings_data

""" create data example if none exists """
if simbatch.prj.total_projects == 0:
    simbatch.create_example_data()


#

""" set definition """
simbatch.dfn.update_current_definition_by_name("Maya")

""" set project """
simbatch.prj.update_current_from_id(simbatch.prj.max_id)

""" set schema """
simbatch.sch.update_current_from_id(simbatch.tsk.tasks_data[-1].schema_id)

""" set task """
simbatch.tsk.update_current_from_id(simbatch.tsk.max_id)

#


""" print basic info """
if show_info is True:
    simbatch.print_important_values()

#


""" clear 'DONE' queue items """
if clear_queue is True:
    simbatch.que.remove_all_queue_items(only_done=True)
    simbatch.que.save_queue()


""" add last task to queue """
if add_single is True:
    new_queue_items = simbatch.que.generate_queue_items(simbatch.tsk.max_id)
    simbatch.que.add_to_queue(new_queue_items)
    simbatch.que.save_queue()


""" add last task to queue with evolutions """
if add_multi is True:
    evo_str = "Bnd 111 222"
    ret = simbatch.pat.get_evolutions_from_string(evo_str)
    new_queue_items = simbatch.que.generate_queue_items(simbatch.tsk.max_id)
    simbatch.que.add_to_queue(new_queue_items)
    simbatch.que.save_queue()


""" add last task to queue with evolutions and user params """
if add_param is True:
    schema_options = simbatch.sch.create_schema_options_object()
    schema_options.set_action_value("Open", "open_file.mb")
    schema_options.set_action_value("Import", "<shot_ani_cache_dir>/orc_*.xml")
    # schema_options.set_action_value("Import", "<project_cache_dir>/captain_sword.xml", occurrence=2)
    schema_options.set_action_value("Save", "custom_file_name_v<ver>.mb")
    # schema_options.set_action_value("Save", "<shot_dir>/backup/<schema_name>_<shot_name>__v<ver>.mb", occurrence=2)
    # schema_options.set_action_value("Save", "<working_dir>/last_sim/last_sim.mb", occurrence=3)

    inputs = []
    inputs.append([simbatch.sio.predefined.convert_predefined_variables_to_values("<schema_base_setup>")])
    inputs.append([simbatch.sio.predefined.convert_predefined_variables_to_values("<shot_ani_cache_dir>")])
    inputs.append([simbatch.sio.predefined.convert_predefined_variables_to_values("<object>.<param>=<value>")])
    inputs.append([simbatch.sio.predefined.convert_predefined_variables_to_values("<cloth_objects>")])
    inputs.append([simbatch.sio.predefined.convert_predefined_variables_to_values("<shot_prev_seq>")])
    inputs.append([simbatch.sio.predefined.convert_predefined_variables_to_values("<copmuted_scene>")])
    inputs.append([simbatch.sio.predefined.convert_predefined_variables_to_values("<scripts_dir>\mmmm.py")])

    simbatch.tsk.increase_queue_ver()

    task_options = simbatch.tsk.create_task_options_object()
    task_options.set_task_value("sim_from", 10)
    task_options.set_task_value("sim_to", 40)
    task_options.set_task_value("prior", 22)
    task_options.set_task_value("user options", 22)
    task_options.set_task_value("user_id", 1)

    new_queue_items = simbatch.que.generate_queue_items(simbatch.tsk.max_id, action_inputs=inputs,
                                                        schema_options=schema_options, task_options=task_options)

    simbatch.que.add_to_queue(new_queue_items)
    simbatch.que.save_queue()



""" print queue info """
if show_info is True:
    simbatch.que.print_header()

""" print last queue item info """
if simbatch.que.total_queue_items > 0:
    simbatch.que.print_queue_item(simbatch.que.queue_data[-1])
