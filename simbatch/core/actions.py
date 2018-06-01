from lib.common import Logger


ACTION_DATA_FIELDS_NAMES = (
    # ('id', 'id'),
    ('name', 'name'),
    # ('type', 'type'),            # "single" or "group",
    ('mode', 'mode'),        # "ANI", "CAM", "OBJ" for 'Import' action
    # ('ui', 'ui'),        # array [["1","2"],["3","4"]]  1 primary button caption 2 function 3 secondary butt 4 sec fun
    ('default', 'default_value'),
    ('actual', 'actual_value'),
    ('template', 'template'),
    ('desc', 'description')
)


class SingleAction:
    """ Single action with template"""
    name = ""
    mode = None
    default_value = ""  # pattern changed when add to queue
    actual_value = ""   # var set by user or default_value, finally used for generate action_script from template
    template = ""       # use template for create absolute ...
    parameters = None   # for nucleus engine it's  BND STR MAS
    description = ""
    json_FIELDS_NAMES = ACTION_DATA_FIELDS_NAMES
    ui = None

    user_value = ""
    logger = None  # TODO  @classmethod


    def __init__(self, name, description, default_value, template, actual_value=None, mode=None, ui=None):
        # self.id = action_id
        self.name = name
        # self.type = type
        self.mode = mode  # subaction mode
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
        return "SingleAction"

    def print_minimum(self):
        print "   action: {}   actual_value: {}".format(self.name, self.actual_value)

    @staticmethod
    def unicode_arr_to_asci_str(arr):
        ret = ""
        for a in arr:
            ret += a
        return ret

    def print_action(self):
        print "   action: {}   default_value: {}   actual_value: {}   template: {}".format(self.name,
                                                                                           self.default_value,
                                                                                           self.actual_value,
                                                                                           self.template)

        self.logger.clear_buffer()
        self.logger.buffering_on()
        logger_raw = self.logger.raw
        logger_raw("   action:          {}\n      default_value: {}\n      actual_value: {}\
                   \n      template:       {}".format(self.name, self.default_value, self.actual_value,
                                                      self.unicode_arr_to_asci_str(self.template)))

        self.logger.buffering_off()
        return self.logger.get_buffer()

    def get_action(self):
        # TODO
        return self

    def get_action_as_string(self):
        # TODO
        return ""

    def complie_action(self, opions):
        # TODO
        return self.template


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
        return "MultiAction"

    def add_single_action(self, new_action):
        if isinstance(new_action, SingleAction):
            self.actions.append(new_action)
            self.actions_count += 1
            return True
        else:
            return False

    def print_actions(self):
        self.logger.clear_buffer()
        self.logger.buffering_on()
        logger_raw = self.logger.raw
        logger_raw("\nname:  {}     total_actions:  {} ".format(self.name, self.actions_count))
        for i, ac in enumerate(self.actions):
            logger_raw("  _action:  {}    desc: {} ".format(ac.name, ac.description))

        self.logger.buffering_off()
        return self.logger.get_buffer()
