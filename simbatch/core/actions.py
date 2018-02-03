
ACTION_DATA_FIELDS_NAMES = [
    ('id', 'id'),
    ('name', 'action_name'),
    ('type', 'action_type'),            # "single" or "group",
    ('sub_mode', 'action_sub_mode'),    # "ANI", "CAM", "OBJ"  for import action
    ('default', 'default_value'),
    ('template', 'template'),
    ('desc', 'description')

    ]


class SingleAction:
    """ Single action is class for store template"""
    id = None
    name = ""
    user_value = ""
    default_value = ""

    def __init__(self, action_id, name, description, default_value, template, mode=None, addi_butt=None, addi_fun=None):
        self.id = action_id
        self.name = name
        self.mode = mode  # subaction mode
        self.description = description
        self.default_value = default_value
        self.template = template

        self.addional_butt_caption = addi_butt
        self.addional_funcion_name = addi_fun

    def __repr__(self):
        return "SingleAction({},{})".format(self.id, self.name)

    def __str__(self):
        return "SingleAction"

    def print_minimum(self, group=False):
        if group:
            prefix = "_"     # obsollette
        else:
            prefix = ""
        print "   {}action: {}   id:{}   default_value:{}".format(prefix, self.name, self.id, self.default_value)

    def print_action(self):
        print "   action: {}   id:{}   description:{} default_value:{}, template:{}".format(self.name, self.id,
                                                                                            self.description,
                                                                                            self.default_value,
                                                                                            self.template)

    def get_action(self):
        return self

    def get_action(self):
        return self

    def get_action_as_string(self):
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
