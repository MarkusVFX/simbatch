#
# For network work and multi node implementation
# please ask about PRO version
#
#  www.SimBatch.com
#
class SimNodes:
    batch = None
    comfun = None

    nodes_data = []
    total_nodes = 0

    current_node_id = None
    current_node_index = None
    current_node = None

    def __init__(self, batch):
        self.batch = batch
        self.comfun = batch.comfun
        self.nodes_data = []

    def print_current(self):
        print " TODO print node"  # TODO print

#
# For network work and multi node implementation
# please ask about PRO version
#
#  www.SimBatch.com
#
