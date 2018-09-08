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

import core.api as simbatchapi

""" init SimBATCH """

api = simbatchapi.SimBatchAPI(ini_file="config.ini")


""" show data source """
if show_info is True:
    print "data dir: ", api.get_data_path()
    print "settings data: ", api.get_settings_path()

""" load data or create example data """
api.load_data()
api.create_example_data_if_not_exists()


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
if add_single is True:
    api.add_current_task_to_queue()


""" add last task to queue with evolutions """
if add_multi is True:
    evo_str = "Bnd 111 222"
    api.add_current_task_to_queue(evo=evo_str)


""" add last task to queue with evolutions and user params """
if add_param is True:
    schema_options = api.get_schema_options_object()
    schema_options.set_action_value("Open", "open_file.mb")
    schema_options.set_action_value("Import", "<shot_ani_cache_dir>/orc_*.xml")
    # schema_options.set_action_value("Import", "<project_cache_dir>/captain_sword.xml", occurrence=2)
    schema_options.set_action_value("Save", "custom_file_name_v<ver>.mb")
    # schema_options.set_action_value("Save", "<shot_dir>/backup/<schema_name>_<shot_name>__v<ver>.mb", occurrence=2)
    # schema_options.set_action_value("Save", "<working_dir>/last_sim/last_sim.mb", occurrence=3)

    user_inputs_object = api.create_inputs_object()
    # TODO user_inputs_object.add
    api.add_user_input("<schema_base_setup>")
    api.add_user_input("<shot_ani_cache_dir>")
    api.add_user_input("<object>.<param>=<value>")
    api.add_user_input("<cloth_objects>")
    api.add_user_input("<shot_prev_seq>")
    api.add_user_input("<copmuted_scene>")
    api.add_user_input("<scripts_dir>\example.py")

    task_options = api.create_task_options_object()
    task_options.set_task_value("sim_from", 10)
    task_options.set_task_value("sim_to", 40)
    task_options.set_task_value("prior", 22)
    task_options.set_task_value("user options", 22)
    task_options.set_task_value("user_id", 1)

    api.add_current_task_to_queue(action_inputs=user_inputs_object, schema_options=schema_options,
                                  task_options=task_options)

""" print queue info """
if show_info is True:
    api.print_queue_header()
    api.print_last_queue_item()
