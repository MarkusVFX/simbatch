class Interaction:
    current_os = -1
    logger = None

    def __init__(self, current_os, logger):
        self.current_os = current_os
        self.logger = logger

    def print_info(self):
        self.logger.raw("This is interaction with Maya")

    # framework interactions
    def schema_item_double_click(self, param):
        self.logger.raw(("Double click on schema item", param))