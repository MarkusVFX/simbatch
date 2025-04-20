import copy
import os

from .lib.common import Logger


ACTION_DATA_FIELDS_NAMES = (
    # ('id', 'id'),
    ('name', 'name'),
    ('evos', 'evos_possible'),            # "single" or "group",
    ('mode', 'mode'),        # "ANI", "CAM", "OBJ" for 'Import' action
    # ('ui', 'ui'),        # array [["1","2"],["3","4"]]  1 primary button caption 2 function 3 secondary butt 4 sec fun
    # ('default', 'default_value'),
    ('actual', 'actual_value'),
    ('template', 'template'),
    ('desc', 'description')
)


class SingleParameter:    # "STR": ["stretch", "stretchResistance", 40, "stretch Resistance"],
    abbrev = ""
    name = ""
    execution_name = ""
    def_val = ""
    description = ""

    def __init__(self, abbrev, name, execution_name, def_val, description):
        self.abbrev = abbrev
        self.name = name
        self.execution_name = execution_name
        self.def_val = def_val
        self.description = description

    def __str__(self):
        return f"SingleParameter    name:{self.name}"

    def print_this(self):
        print(f"   {self.abbrev}   name: {self.name}")


class ActionParameters:
    name = None
    template = None
    param_list = None

    def __init__(self, name, template):
        self.name = name
        self.template = template
        self.param_list = []

    def print_params(self):
        for p in self.param_list:
            print(f"  {p.abbrev}  _  {p.name}   __   {p.description}    ___  {p.execution_name}")

    def add_param_to_list(self, abbrev, name, execution_name, def_val, description):
        self.param_list.append(SingleParameter(abbrev, name, execution_name, def_val, description))

    def get_execution_name_by_abbrev(self, abbr):
        for p in self.param_list:
            if p.abbrev == abbr:
                return p.execution_name


class SingleAction:
    """ Single action with template"""
    name = ""
    evos_possible = False  # True for sim engines with evolutions possible BND, DMP, ...
    mode = None         # nCloth, nHair, Fume ... for Maya simulate ; BLAST, RENDER for prev; (defined in definitions)
    # default_value = ""  # template is a def val !!!
    actual_value = ""   # var set by user or default_value, finally used for generate action_script from template
    template = ""       # use template for create absolute script (defined in definitions)
    parameters = None   # for nucleus engine it's  BND STR MAS (defined in definitions)
    description = ""
    json_FIELDS_NAMES = ACTION_DATA_FIELDS_NAMES
    ui = None

    user_value = ""
    logger = None  # TODO  @classmethod

    def __init__(self, name, description, template, actual_value=None, mode=None, ui=None, evos_possible=False):
        self.name = name
        self.evos_possible = evos_possible
        self.mode = mode  # subaction mode : nCloth, nHair, Fume
        if ui is None:
            self.ui = ["None"]
        else:
            self.ui = ui
        self.description = description
        # old self.default_value = default_value
        if actual_value is not None:
            self.actual_value = actual_value
        self.template = template

        self.logger = Logger()

    def __repr__(self):
        return f'SingleAction("{self.name}", "{self.description}", "{self.template}", actual_value="{self.actual_value}", ui="{self.ui}")'

    def __str__(self):
        return f"SingleAction {self.name} {self.description} {self.template}"

    def print_this(self):
        print(f"   action: {self.name}   actual_value: {self.actual_value}")

    def set_evos_possible(self, bool_val):
        self.evos_possible = bool_val

    def str_arr_to_str(self, arr):    # TODO std lib !
        ret = ""
        for s in arr:
            ret += s
        return ret

    def print_this(self):
        print(f"   action: {self.name}   def_val: {self.ui[0]}   actual_val: {self.actual_value}   templ: {self.template}   mode: {self.mode}")
        print(f"   template: {self.str_arr_to_str(self.template)}")

    """
    def get_action(self):
        # TODO
        return self

    def get_action_as_string(self):
        # TODO
        return ""
    """

    """ marker ATQ 235   generate script from temlpate   """
    def generate_script_from_action_template(self, batch, option, with_new_line=False, evo="", task_id=""):
        # TODO optimize + mixed var     <dir>\custom_file.bin
        template_with_values = copy.deepcopy(self.template)
        for i, twv in enumerate(template_with_values):
            if twv[0] == "<":
                if twv == "<ui>":
                    if len(option) > 0:
                        if "^" in option:
                            template_with_values[i] = option.split("^")[0]
                        else:
                            template_with_values[i] = option
                    else:
                        template_with_values[i] = "empty_option"
                else:
                    template_with_values[i] = batch.sio.predefined.convert_predefined_variables_to_values(twv, param=evo, option=task_id)
                template_with_values[i] = "\"" + template_with_values[i] + "\""
        scr = "".join(template_with_values)
        if with_new_line:
            scr += os.linesep
        return scr


class MultiAction:
    """
    Grouped actions class is container for ONE or more SingleAction objects
    this container grouping similar actions, few actions of one type  or different versions of actions
    """
    multi_id = None
    name = ""
    actions = []  # one or more SingleAction objects
    actions_count = 0
    logger = None

    def __init__(self, multi_id, name):
        self.multi_id = multi_id
        self.name = name
        self.actions = []
        self.logger = Logger()

    def __repr__(self):
        return f"MultiAction({self.multi_id},{self.name})"

    def __str__(self):
        return f"MultiAction  name:{self.name}"

    def print_actions(self):
        self.logger.clear_buffer()
        self.logger.buffering_on()
        logger_raw = self.logger.raw
        logger_raw(f"{os.linesep}name:  {self.name}     total_actions:  {self.actions_count} ")
        for i, ac in enumerate(self.actions):
            logger_raw(f"   action:  {ac.name}    desc: {ac.description} ")

        self.logger.buffering_off()
        return self.logger.get_buffer()

    def add_single_action(self, new_action):
        if isinstance(new_action, SingleAction):
            self.actions.append(new_action)
            self.actions_count += 1
            return True
        else:
            return False

    def get_action_index_by_mode(self, mode):
        for i, a in enumerate(self.actions):
            if a.mode == mode:
                return i
        return None


class Actions:
    """Class to manage all actions"""
    batch = None
    comfun = None
    logger = None

    def __init__(self, batch):
        self.batch = batch
        self.comfun = batch.comfun
        self.logger = batch.logger

    def get_action_by_name(self, name):
        """Get action by name"""
        # TODO: Implement action lookup logic
        return None

    def get_actions_list(self):
        """Get list of all available actions"""
        # TODO: Implement action list retrieval
        return []

    def print_actions(self):
        """Print all available actions"""
        actions = self.get_actions_list()
        if not actions:
            print("No actions available")
            return
        for action in actions:
            print(f"Action: {action.name}")
            print(f"  Description: {action.description}")
            print(f"  Template: {action.template}")
            print("---")
