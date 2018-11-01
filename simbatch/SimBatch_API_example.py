# simbatch_no_gui_exampple

show_info = False

add_to_queue_single = False
add_to_queue_multi = False
add_to_queue_with_param = True

clear_queue = True

#
##
###
#####
########
################
########################

import core.api as simbatchapi

""" init SimBATCH """

api = simbatchapi.SimBatchAPI(ini_file="config.ini")


""" show settings and data source """
if show_info is True:
    print "settings data: ", api.get_settings_path()
    print "data dir: ", api.get_data_path()

""" load data or create example data """
api.load_data()
api.create_example_data_if_not_exists()
api.create_api_example_if_not_exists()

""" set working data """
api.set_current_definition("Maya")
api.set_current_project(last=True)
api.set_current_schema(last=True)
api.set_current_task(last=True)

""" print basic info """
if show_info is True:
    api.print_basic_data_info()

#

""" clear 'DONE' queue items """
if clear_queue is True:
    api.clear_green_items_from_queue()

""" add last task to queue """
if add_to_queue_single is True:
    api.add_current_task_to_queue()


""" add last task to queue with evolutions """
if add_to_queue_multi is True:
    evo_str = "BND 111 222"
    api.add_current_task_to_queue(evo=evo_str)


""" add last task to queue with evolutions and user params """
if add_to_queue_with_param is True:
    schema_options = api.get_schema_options_object()
    schema_options.set_action_value("Open", "open_file.mb")
    schema_options.set_action_value("Import", "<shot_ani_cache_dir>/orc_*.xml")
    # schema_options.set_action_value("Import", "<project_cache_dir>/captain_sword.xml", occurrence=2)
    schema_options.set_action_value("Save", "custom_file_name_v<ver>.mb")
    # schema_options.set_action_value("Save", "<shot_dir>/backup/<schema_name>_<shot_name>__v<ver>.mb", occurrence=2)
    # schema_options.set_action_value("Save", "<working_dir>/last_sim/last_sim.mb", occurrence=3)

    task_options = api.create_task_options_object()
    task_options.set_task_value("sim_frame_start", 10)
    task_options.set_task_value("sim_frame_end", 40)
    task_options.set_task_value("prev_frame_start", 22)
    task_options.set_task_value("prev_frame_end", 40)
    task_options.set_task_value("priority", 22)
    task_options.set_task_value("options", "inplace")

    # api.simbatch_core.tsk.print_task(task_options.proxy_task)

    api.add_current_task_to_queue(schema_options=schema_options, task_options=task_options)

# show_info = True

""" print queue info """
if show_info is True:
    api.print_queue_info()
    api.print_last_queue_item()

