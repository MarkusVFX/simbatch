try:  # Maya 2016
    from PySide.QtCore import *
    from PySide.QtGui import *
except ImportError:
    try:  # Maya 2017
        from PySide2.QtCore import *
        from PySide2.QtGui import *
        from PySide2.QtWidgets import *
    except ImportError:
        raise Exception('PySide import ERROR!  Please install PySide or PySide2')

from widgets import *


class DefinitionsUI:
    qt_widget_definitions = None
    qt_lay_definitions_main = None

    current_selected = [0,0,0]

    batch = None
    top_ui = None
    mainw = None

    comfun = None

    def __init__(self, batch, mainw, top):
        self.batch = batch
        self.comfun = batch.comfun

        self.dfn = batch.dfn
        self.sts = batch.sts

        self.top_ui = top
        self.mainw = mainw
        self.init_ui()

    def init_ui(self):
        qt_widget_definitions = QWidget()
        qt_widget_definitions.setContentsMargins(0, 0, 0, 0)

        self.qt_widget_definitions = qt_widget_definitions

        qt_lay_definitions_main = QVBoxLayout(qt_widget_definitions)
        qt_lay_definitions_main.setContentsMargins(0, 0, 0, 0)
        self.qt_lay_definitions_main = qt_lay_definitions_main

        qt_tree_lay = QVBoxLayout()
        qt_definitions_tree = QTreeWidget()
        qt_definitions_tree.setColumnCount(4)
        qt_definitions_tree.setColumnWidth(0, 150)
        qt_definitions_tree.setColumnWidth(1, 40)
        qt_definitions_tree.setColumnWidth(2, 70)
        # qt_definitions_tree.setHeaderHidden(True)
        qt_definitions_tree.setHeaderLabels(["Name", "ID", "elments", "description"])
        qt_definitions_tree.currentItemChanged.connect(self.on_definitions_tree_changed)
        self.qt_definitions_tree = qt_definitions_tree
        qt_tree_lay.addWidget(qt_definitions_tree)

        qt_print_lay = QVBoxLayout()
        qt_print_lay_A = QHBoxLayout()
        qt_print_lay_B = QHBoxLayout()
        # current_name = EditLineWithButtons("Project Name:", label_minimum_size=94)
        qt_current = EditLineWithButtons("Current:")
        self.qt_current = qt_current
        qt_print_base = ButtonOnLayout("Definitons")
        qt_print_current = ButtonOnLayout("Print Selected")
        qt_print_all = ButtonOnLayout("Print ALL")
        qt_clear_info = ButtonOnLayout("Clear Info")

        qt_print_base.button.clicked.connect(self.on_click_print_base)
        qt_print_current.button.clicked.connect(self.on_click_print_current)
        qt_print_all.button.clicked.connect(self.on_click_print_all)
        qt_clear_info.button.clicked.connect(self.on_click_clear_info)

        self.comfun.add_layouts(qt_print_lay_A, [qt_current.qt_widget_layout])
        self.comfun.add_layouts(qt_print_lay_B, [qt_print_base.qt_widget_layout,
                                                 qt_print_current.qt_widget_layout,
                                                 qt_print_all.qt_widget_layout,
                                                 qt_clear_info.qt_widget_layout])
        qt_print_lay.addLayout(qt_print_lay_A)
        qt_print_lay.addLayout(qt_print_lay_B)

        qt_show_lay = QVBoxLayout()
        qt_definition_content = QTextEdit()
        qt_definition_content.setText("Definition detailed info:")
        self.qt_definition_content = qt_definition_content
        qt_show_lay.addWidget(qt_definition_content)

        self.comfun.add_layouts(qt_lay_definitions_main, [qt_show_lay, qt_tree_lay, qt_print_lay])
        self.init_tree()

    def init_tree(self):
        tree = self.qt_definitions_tree
        qt_light_brush = QBrush(QColor.fromRgb(0, 70, 140, a=255))
        qt_dark_brush = QBrush(QColor.fromRgb(0, 90, 22, a=255))
        for i, de in enumerate(self.dfn.definitions_names):
            tree_item_soft = QTreeWidgetItem()
            tree_item_soft.setText(0, de)
            tree_item_soft.setText(1, str(i))
            tree_item_soft.setText(2, str(self.dfn.definitions_array[i].total_actions))
            for j, ac in enumerate(self.dfn.definitions_array[i].action_names):
                tree_child_action = QTreeWidgetItem(tree_item_soft)
                tree_child_action.setText(0, ac)
                tree_child_action.setText(1, str(j))
                if self.dfn.definitions_array[i].multi_actions_array[j].actions_count > 0:
                    tree_child_action.setText(2, str(self.dfn.definitions_array[i].multi_actions_array[j].actions_count))


                tree_child_action.setForeground(0, qt_dark_brush)
                tree_child_action.setForeground(1, qt_dark_brush)
                tree_child_action.setForeground(2, qt_dark_brush)

                for k, sa in enumerate(self.dfn.definitions_array[i].multi_actions_array[j].actions):
                    tree_child_subaction = QTreeWidgetItem(tree_child_action)
                    tree_child_subaction.setText(0, ac)
                    tree_child_subaction.setText(1, str(k))
                    tree_child_subaction.setText(3, sa.description)
                    tree_child_subaction.setForeground(0, qt_light_brush)
                    tree_child_subaction.setForeground(1, qt_light_brush)
                # tree_item.addChild(tree_child)
            tree.addTopLevelItem(tree_item_soft)

    def on_definitions_tree_changed(self, new, old):
        if new is not None:
            parent_id = None
            parent_parent_id = None
            full_path_element = new.text(0)
            root_id = new.text(1)
            # parent_str = ""
            # parent_parent_str = ""
            parent = new.parent()
            if parent is not None:
                parent_str = parent.text(0)

                parent_id = root_id
                root_id = parent.text(1)

                full_path_element = "{}    {}".format(parent_str, full_path_element)
                parent_parent = parent.parent()
                if parent_parent is not None:
                    parent_parent_str = parent_parent.text(0)

                    parent_parent_id = parent_id
                    parent_id = root_id
                    root_id = parent_parent.text(1)

                    full_path_element = "{}    {}   {}{}{}".format(parent_parent_str, full_path_element,
                                                                   "[", new.text(1), "]")

            self.qt_current.qt_edit_line.setText(full_path_element)
            self.current_selected = [self.batch.comfun.int_or_val(root_id, None),
                                     self.batch.comfun.int_or_val(parent_id, None),
                                     self.batch.comfun.int_or_val(parent_parent_id, None)]

    def print_to_definition_info(self, txt):
        logger_raw = self.batch.logger.raw
        self.qt_definition_content.append(txt)
        logger_raw(txt)

    def on_click_print_base(self):

        if self.dfn.current_definition_name is None:
            self.print_to_definition_info("\n total_defn:{} current:None".format(self.dfn.total_definitions))
        else:
            self.print_to_definition_info("\n total_defn:{} current:{}".format(self.dfn.total_definitions,
                                                                               self.dfn.current_definition_name))
            self.print_to_definition_info(" dfn count:{} dfn names count:{}".format(len(self.dfn.definitions_array),
                                                                                    len(self.dfn.definitions_names)))
        for d in self.dfn.definitions_array:
            self.print_to_definition_info(" _name:{} total_actions:{} names count:{}".format(d.name, d.total_actions,
                                                                                             len(d.action_names)))
        self.qt_definition_content.append("\n\n\n")

    def on_click_print_current(self):
        if self.current_selected[0] is not None:
            indexes = self.current_selected
            self.print_to_definition_info("Current definition :  {}".format(self.dfn.definitions_names[indexes[0]]))
            if len(indexes) > 1:
                self.print_to_definition_info(" Current action :  {}".format(
                    self.dfn.definitions_array[indexes[0]].action_names[indexes[1]]))
            if len(indexes) > 2:
                self.print_to_definition_info("  Current subaction :  {}".format(
                    self.dfn.definitions_array[indexes[0]].multi_actions_array[indexes[1]].actions[indexes[2]].name))

            if len(indexes) == 1:
                d = self.dfn.definitions_array[indexes[0]]
                self.qt_definition_content.append(d.print_single())
            elif len(indexes) == 2:
                ma = self.dfn.definitions_array[indexes[0]].multi_actions_array[indexes[1]]
                self.qt_definition_content.append(ma.print_actions())
            else:
                sa = self.dfn.definitions_array[indexes[0]].multi_actions_array[indexes[1]].actions[indexes[2]]
                self.qt_definition_content.append(sa.print_action())
            self.qt_definition_content.append("\n\n\n")
        else:
            self.top_ui.set_top_info("Select element from tree view", 7)

    def on_click_print_all(self):
        for d in self.dfn.definitions_array:
            self.qt_definition_content.append("\n")
            self.qt_definition_content.append(d.print_single())

        self.qt_definition_content.append("\n\n\n")

    def on_click_clear_info(self):
        self.qt_definition_content.setText("")
