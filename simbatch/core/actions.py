from lib.common import Logger


ACTION_DATA_FIELDS_NAMES = (
    # ('id', 'id'),
    ('name', 'name'),
    ('evos', 'evos_possible'),            # "single" or "group",
    ('mode', 'mode'),        # "ANI", "CAM", "OBJ" for 'Import' action
    # ('ui', 'ui'),        # array [["1","2"],["3","4"]]  1 primary button caption 2 function 3 secondary butt 4 sec fun
    ('default', 'default_value'),
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
        return "SingleParameter    name:" + self.name

    def print_minimum(self):
        print "   {}   name: {}".format(self.abbrev, self.name)


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
            print "  {}   {}      {}".format(p.abbrev, p.name, p.description)

    def add_param_to_list(self, abbrev, name, execution_name, def_val, description):
        self.param_list.append(SingleParameter(abbrev, name, execution_name, def_val, description))


class SingleAction:
    """ Single action with template"""
    name = ""
    evos_possible = False  # True for sim engines with evolutions possible BND, DMP, ...
    mode = None         # one of nCloth, nHair, Fume ...   for Maya simulate    BLAST, RENDER for prev
    default_value = ""  # pattern changed when add to queue
    actual_value = ""   # var set by user or default_value, finally used for generate action_script from template
    template = ""       # use template for create absolute ...
    parameters = None   # for nucleus engine it's  BND STR MAS
    description = ""
    json_FIELDS_NAMES = ACTION_DATA_FIELDS_NAMES
    ui = None

    user_value = ""
    logger = None  # TODO  @classmethod

    def __init__(self, name, description, default_value, template, actual_value=None, mode=None, ui=None,
                 evos_possible=False):
        self.name = name
        self.evos_possible = evos_possible
        self.mode = mode  # subaction mode : nCloth, nHair, Fume
        self.ui = ui
        self.description = description
        self.default_value = default_value
        if actual_value is not None:
            self.actual_value = actual_value
        self.template = template

        self.logger = Logger()

    def __repr__(self):
        return 'SingleAction("{}", "{}", "{}", "{}", actual_value="{}", ui="{}")'.format(self.name, self.description,
                                                                                         self.default_value,
                                                                                         self.template,
                                                                                         self.actual_value, self.ui)

    def __str__(self):
        return "SingleAction  " + self.name

    def print_minimum(self):
        print "   action: {}   actual_value: {}".format(self.name, self.actual_value)

    def set_evos_possible(self, bool_val):
        self.evos_possible = bool_val

    @staticmethod
    def unicode_arr_to_asci_str(arr):    # TODO std lib !
        ret = ""
        for a in arr:
            ret += a
        return ret

    def print_action(self):
        print "   action: {}   def_val: {}   actual_val: {}   templ: {}   mode: {}".format(self.name,
                                                                                           self.default_value,
                                                                                           self.actual_value,
                                                                                           self.template,
                                                                                           self.mode)

        self.logger.clear_buffer()
        self.logger.buffering_on()
        logger_raw = self.logger.raw
        logger_raw("   action:          {}\n      default_value: {}\n      actual_value: {}\
                   \n      template:       {}".format(self.name, self.default_value, self.actual_value,
                                                      self.unicode_arr_to_asci_str(self.template)))

        self.logger.buffering_off()
        return self.logger.get_buffer()

    """
    def get_action(self):
        # TODO
        return self

    def get_action_as_string(self):
        # TODO
        return ""
    """

    """ marker ATQ 235   generate script from temlpate   """
    def generate_script_from_template(self, batch, with_new_line=False):
        # TODO optimize + mixed var     <dir>\custom_file.bin
        scr = "".join(self.template)
        if with_new_line:
            scr += "\n"
        return scr


class MultiAction:    # old GroupedActions
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
        return "MultiAction({},{})".format(self.name, self.name)

    def __str__(self):
        return "MultiAction  name:" + self.name

    def print_actions(self):
        self.logger.clear_buffer()
        self.logger.buffering_on()
        logger_raw = self.logger.raw
        logger_raw("\nname:  {}     total_actions:  {} ".format(self.name, self.actions_count))
        for i, ac in enumerate(self.actions):
            logger_raw("   action:  {}    desc: {} ".format(ac.name, ac.description))

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
