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

    @staticmethod
    def print_current():
        if self.current_node_index is not None and self.current_node_index >0:
            n = self.nodes_data[self.current_node_index]
            print " node: ", n.nodeName, n.state, n.description     # TODO   logger print
        else:
            print " no current node, index: ", self.current_node_index     # TODO   logger print

        def load_nodes_from_json(self, json_file=""):
            if len(json_file) == 0:
                json_file = self.batch.sts.store_data_json_directory + self.batch.sts.JSON_SIMNODES_FILE_NAME
            if self.comfun.file_exists(json_file, info="simnodes file"):
                self.batch.logger.inf(("loading simnode items: ", json_file))
                json_nodes = self.comfun.load_json_file(json_file)
                if json_nodes is not None and "simnodes" in json_nodes.keys():
                    if json_nodes['simnodes']['meta']['total'] > 0:
                        for li in json_nodes['simnodes']['data'].values():
                            if len(li) == len(NODES_ITEM_FIELDS_NAMES):
                                new_simnode_item = SingleNode(int(li['id']), li['name'], li['state'],
                                                              int(li['stateId']), li['stateFile'], li['desc'])
                                self.add_simnode(new_simnode_item)
                            else:
                                self.batch.logger.wrn(("simnode json data not consistent:", len(li),
                                                       len(NODES_ITEM_FIELDS_NAMES)))
                        return True
                else:
                    self.batch.logger.wrn(("no tasks data in : ", json_file))
                    return False
            else:
                self.batch.logger.wrn(("no schema file: ", json_file))
                return False

#
# For network work and multi node implementation
# please ask about PRO version
#
#  www.SimBatch.com
#
