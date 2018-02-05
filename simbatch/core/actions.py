
ACTION_DATA_FIELDS_NAMES = (
    ('id', 'id'),
    ('name', 'name'),
    ('type', 'type'),            # "single" or "group",
    ('mode', 'mode'),        # "ANI", "CAM", "OBJ" for 'Import' action
    ('ui', 'ui'),        # array [["1","2"],["3","4"]]  1 primary button caption 2 function 3 secondary butt 4 sec fun
    ('default', 'default_value'),
    ('template', 'template'),
    ('desc', 'description')
)


class SingleAction:
    """ Single action is class for store template"""
    id = None
    name = ""
    type = None
    mode = None
    default_value = ""
    json_FIELDS_NAMES = ACTION_DATA_FIELDS_NAMES
    ui = None                       # store ui for quick save
    # standard_butt_caption = None    # store ui for ui forms
    # standard_funcion_str = None     # store ui for ui forms
    # addional_butt_caption = None    # store ui for ui forms
    # addional_funcion_str = None     # store ui for ui forms

    user_value = ""   # var set by user for generate action_script using template

    def __init__(self, action_id, name, description, default_value, template, type=None, mode=None, ui=None):
        self.id = action_id
        self.name = name
        self.type = type
        self.mode = mode  # subaction mode
        self.ui = ui
        self.description = description
        self.default_value = default_value
        self.template = template

        # if len(ui) > 0:
        #     self.standard_butt_caption = ui[0][0]
        #     self.standard_funcion_str = ui[0][1]
        # if len(ui) > 1:
        #     self.addional_butt_caption = ui[1][0]
        #     self.addional_funcion_str = ui[1][1]

    def __repr__(self):
        return "SingleAction({},{})".format(self.id, self.name)

    def __str__(self):
        return "SingleAction"

    def print_minimum(self, group=False):
        if group:
            prefix = "_"     # obsollette  # TODO cleanup
        else:
            prefix = ""
        print "   {}action: {}   id:{}   default_value:{}".format(prefix, self.name, self.id, self.default_value)

    def print_action(self):
        print "   action: {}   id:{}   description:{} default_value:{}, template:{}".format(self.name,
                                                                                            self.id,
                                                                                            self.description,
                                                                                            self.default_value,
                                                                                            self.template)
    def get_action(self):
        # TODO
        return self

    def get_action(self):
        # TODO
        return self

    def get_action_as_string(self):
        # TODO
        return ""

    def complie_action(self, opions):
        # TODO
        return self.template


class GroupedActions:
    """
    Grouped actions class is container for ONE or more SingleAction objects
    this container grouping similar actions, few actions of one type  or different versions of actions
    """
    group_id = None
    name = ""
    actions = []  # one or more SingleAction objects
    actions_count = 0

    def __init__(self, group_id, name):
        self.group_id = group_id
        self.name = name
        self.actions = []

    def __repr__(self):
        return "GroupedActions({},{})".format(self.name, self.name)

    def __str__(self):
        return "GroupedActions"

    def add_single_action(self, new_action):
        if isinstance(new_action, SingleAction):
            self.actions.append(new_action)
            self.actions_count += 1
            return True
        else:
            return False
