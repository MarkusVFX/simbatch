
ACTION_DATA_FIELDS_NAMES = [
    ('id', 'id'),
    ('name', 'action_name'),
    ('type', 'action_type'),
    ('sub_type', 'action_sub_type'),
    ('param', 'action_param'),
    ('soft_id', 'soft_id')
    ]



class SingleAction:
    id = None
    name = ""

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
        return "SingleAction({},{})".format(self.action_id, self.name)

    def __str__(self):
        return "SingleAction"

    def print_minimum(self,group=False):
        if group:
            prefix = "_"     # obsollette
        else:
            prefix=""
        print "   {}action: {}   id:{}   default_value:{}".format(prefix,self.name, self.id, self.default_value)

    def print_action(self):
        print "   action: {}   id:{}   description:{} default_value:{}, template:{}".format(self.name, self.id,
                                                                                            self.description,
                                                                                            self.default_value,
                                                                                            self.template)

    def get_action(self):
        return self

    def get_action_as_string(self):
        return ""



class GroupedActions:
    group_id = None
    name = ""
    actions = []  # one or more SingleAction objects
    actions_count = 0
    # current_sub_action_index = 0

    def __init__(self, group_id, name):
        self.group_id = group_id
        self.name = name
        self.actions = []
        self.actions_count = 1

    def __repr__(self):
        return "GroupedActions({},{})".format(self.name, self.name)

    def __str__(self):
        return "GroupedActions"

    # def get_action(self):
    #     return self.actions[self.current_sub_action_index]