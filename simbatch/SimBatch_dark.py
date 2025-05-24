import sys, errno

try:
    from PySide2.QtGui import *
    from PySide2.QtWidgets import QApplication
    from PySide2.QtCore import Qt
except ImportError:
    print ("\n\n  PySide import ERROR!\n  Please install PySide or PySide2\n  pip install -U PySide")
    sys.exit(errno.EACCES)

import core.core as core
import ui.mainw as ui
import server.server as simbatch_server

app = QApplication([])

# Set dark mode
app.setStyle("Fusion")
dark_palette = QPalette()
dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
dark_palette.setColor(QPalette.WindowText, Qt.white)
dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
dark_palette.setColor(QPalette.ToolTipText, Qt.white)
dark_palette.setColor(QPalette.Text, Qt.white)
dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
dark_palette.setColor(QPalette.ButtonText, Qt.white)
dark_palette.setColor(QPalette.BrightText, Qt.red)
dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
dark_palette.setColor(QPalette.HighlightedText, Qt.black)
app.setPalette(dark_palette)

simbatch = core.SimBatch("Stand-alone")   # for custom startup vals add optional argument: ini_file="your_config.json"
loading_data_state = simbatch.load_data()
server = simbatch_server.SimBatchServer(simbatch, framework_mode=True)

if simbatch.sts.with_gui == 1:
    main_window = ui.MainWindow(server)
    main_window.show()
    main_window.post_run(loading_data_state)

app.exec_()
