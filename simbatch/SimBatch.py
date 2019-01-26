import sys, errno

try:
	from PySide.QtGui import *
except ImportError:
    print "\n\n  PySide import ERROR!\n  Please install PySide or PySide2\n  It's easy run commands:\n    cd your_pip_directory\n    pip install -U PySide"
    sys.exit(errno.EACCES)

import core.core as core
import ui.mainw as ui
import server.server as simbatch_server

app = QApplication([])

simbatch = core.SimBatch("Stand-alone")   # you can set startup config by adding optional argument: ini_file="your_config.json"
loading_data_state = simbatch.load_data()
server = simbatch_server.SimBatchServer(simbatch, framework_mode=True)


if simbatch.sts.with_gui == 1:
    main_window = ui.MainWindow(server)
    main_window.show()
    main_window.post_run(loading_data_state)

app.exec_()
