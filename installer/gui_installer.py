import sys
import os
import platform
import time
import random

if __name__ == '__main__' and __package__ is None:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simbatch.core.lib.logger import Logger
from simbatch.core.lib.common import CommonFunctions


try:
    from PySide.QtCore import *
    from PySide.QtGui import *
except ImportError:
    try:
        from PySide2.QtCore import *
        from PySide2.QtGui import *
        from PySide2.QtWidgets import *
    except ImportError:
        raise Exception('PySide import ERROR!  Please install PySide or PySide2')

env_maya = False

try:
    import maya.OpenMayaUI as mui
    env_maya = True
except ImportError:
    print('OpenMayaUI import ERROR! Run this script from Maya')
    pass


def getMayaWindow():
    pointer = mui.MQtUtil.mainWindow()
    return shiboken.wrapInstance(long(pointer), QtGui.QWidget)

try:    # Maya 2016
    import shiboken
except:
    try:  # Maya 2017
        import shiboken2 as shiboken
    except:
        print "shiboken import ERROR"
        pass



class AnimatedBar(QWidget):
    anim_data = None
    welcome_text = "SimBatch Installer"
    comfun = None
    qt_painter = None
    anim_state = 0
    current_frame = None
    current_frame_index = 0
    cursor_index = 0
    anim_data_length = 0
    canvas = None
    grayscale_4_colors = None
    play_start = 0
    

    def __init__(self, comfun):
        super(AnimatedBar, self).__init__()
        self.comfun = comfun
        qt_font = QFont()
        qt_font.setPointSize(10)
        qt_font.setBold(True)
        qt_font.setFamily("Veranda")
        qt_lbl_info = QLabel("info")
        qt_lbl_info.setFont(qt_font)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_next_frame)
        self.grayscale_4_colors = (QColor(0, 0, 0), QColor(42, 42, 42), QColor(84, 84, 84), QColor(127, 127, 127))

    def paintEvent(self, event):
        qt_painter = QPainter()
        self.qt_painter = qt_painter
        qt_painter.begin(self)
        if self.anim_state == 1:
            self.draw_single_anim_frame(event, qt_painter, double = self.canvas[4], pix_size=self.canvas[5], pix_offset=self.canvas[6])

            self.anim_state = 2
        else:
            self.draw_welcome_text(event, qt_painter)
        qt_painter.end()

    def draw_welcome_text(self, event, qt_painter):
        qt_painter.setPen(QColor(130, 150, 170))
        qt_font = QFont('Veranda', 22)
        qt_font.setBold(True)
        qt_painter.setFont(qt_font)
        qt_painter.drawText(event.rect(), Qt.AlignCenter, self.welcome_text)

    def draw_single_anim_frame(self, event, qt_painter, double = False, pix_size=4, pix_offset=5):
        
        pen=qt_painter.pen()
        pen.setStyle(Qt.NoPen)
        qt_painter.setPen(pen)

        cf = self.current_frame
        if cf[0] % 2 == 0 :
            qt_painter.setBrush(self.grayscale_4_colors[0])
        else:
            qt_painter.setBrush(self.grayscale_4_colors[2])
        qt_painter.drawRect(pix_offset, pix_offset, pix_size, pix_size)
        if cf[0] % 4 == 0 :
            qt_painter.setBrush(self.grayscale_4_colors[1])
        else:
            qt_painter.setBrush(self.grayscale_4_colors[3])
        qt_painter.drawRect(pix_offset, pix_offset*2, pix_size, pix_size)

        # create pix
        for i, el_i in enumerate(cf[1]):
            for j, el_j in enumerate(el_i):
                # print "fr:", cf[0], "  ___ ",i, j ,  "  ___ ", el_j[0], el_j[1], "   _ ", len(self.canvas[2])
                qt_painter.setBrush(self.canvas[2][el_j[0]])
                qt_painter.drawRect(pix_offset*j+pix_offset*2, pix_offset * i, pix_size, pix_size)

                if double:
                    qt_painter.setBrush(self.canvas[2][el_j[1]])
                    qt_painter.drawRect(pix_offset*j+pix_offset*2, pix_offset * i +pix_offset*(self.canvas[0]), pix_size, pix_size)

    def show_next_frame(self):  # triggered by timer !!!!
        w_len = self.canvas[0]*self.canvas[1]
        if self.cursor_index < self.anim_data_length - w_len:

            i_arr = []
            for i in range(0,self.canvas[0]):
                j_arr = []
                for j in range(0,self.canvas[1]):
                    intchar = ord(self.anim_data[self.cursor_index + i*self.canvas[0] + j])
                    
                    # debug
                    # print "db:[{}] [{}]".format(  self.anim_data[self.cursor_index + i*self.canvas[0] + j], intchar) 
                    
                    offset = 0
                    while intchar > self.canvas[3]-1:
                        offset +=1
                        intchar -= self.canvas[3]-1

                    j_arr.append((offset, intchar))
                    
                    # debug
                    # print "          [{}] [{}]\n".format(intchar, offset) 
                i_arr.append(j_arr)
            # self.current_frame = ord(self.anim_data[self.current_frame_index])
            frame = []

            self.current_frame = (self.current_frame_index, i_arr)
            self.cursor_index += w_len
            self.current_frame_index += 1

            self.anim_state = 1
            self.update()
        else:
            self.timer.stop()
            play_time = time.time()
            print "play time : ", play_time - self.play_start

    def get_random_color_palette(self, length):
        p=[]
        for i in range(0,length):
            #p.append(QColor(random.randint(0,127),random.randint(0,127),random.randint(0,127)))
            colo = i * 12
            p.append(QColor(colo,colo,colo))
        return p
        
    def get_my_color_palette(self):
        p=[]
        colors_arr = ("3f32ae","efe305","e30ec2","baaaff","ffffff","bb0200","000000","6a8927","16ed75","057fc1","c98f4c","efe305")
        for c in colors_arr:
            p.append(QColor("#"+c))
        return p

    def play_anim_data(self, qt_painter, anim_data):
        self.timer.start(self.delay)
        
    def set_anim_format(self, a_height=4, a_widht=40, delay=100, double=False, pix_size=4, pix_offset=5):
        # number_of_colors = 13
        # color_palette = self.get_random_color_palette(number_of_colors)
        color_palette = self.get_my_color_palette()
        self.canvas = (a_height, a_widht, color_palette, len(color_palette), double, pix_size, pix_offset)
        self.delay = delay

    def load_anim(self, data):
        self.anim_data = data
        self.anim_data_length = len(data)
        self.current_frame_index = 0
        self.cursor_index = 0
        
    def play_anim(self):
        self.play_start = time.time()
        self.play_anim_data(self.qt_painter, self.anim_data)



class InstallerWindow(QMainWindow):
    top_ui = None
    qt_tab_widget = None
    window_height = 400
    window_width = 550

    animated_bar = None
    comfun = None

    dir_separator = "/"

    def __init__(self, w , h):
        super(InstallerWindow, self).__init__()
        if platform.system() == "Windows":
            self.dir_separator = "\\"

        self.window_height = h
        self.window_width = w
        self.init_ui()

    def init_ui(self):
        self.logger = Logger(log_level=0, console_level=3)
        self.comfun = CommonFunctions(self.logger)
        self.setMinimumHeight(self.window_height)
        self.setMinimumWidth(self.window_width)

        self.animated_bar = AnimatedBar(self.comfun)

        qt_central_widget = QWidget(self)
        qt_lay_central = QVBoxLayout()
        qt_lay_central.setContentsMargins(0, 0, 0, 0)
        qt_central_widget.setLayout(qt_lay_central)

        qt_lay_paths = QVBoxLayout()
        qt_gbox_paths = QGroupBox()
        qt_gbox_paths.setLayout(qt_lay_paths)
        """ SOURCE """
        qt_lay_path_source = QHBoxLayout()
        qt_path_source_label = QLabel("Source directory : ")
        qt_path_source_edit = QLineEdit("")
        self.qt_path_source_edit = qt_path_source_edit
        qt_path_source_button = QPushButton("Get")
        qt_path_source_button.setToolTip('Select directory')
        qt_path_source_button.clicked.connect(self.on_click_get_source_dir)
        qt_lay_path_source.addWidget(qt_path_source_label)
        qt_lay_path_source.addWidget(qt_path_source_edit)
        qt_lay_path_source.addWidget(qt_path_source_button)

        """ DEST """
        qt_lay_path_destination = QHBoxLayout()
        qt_path_destination_label = QLabel("Destination directory : ")
        qt_path_destination_edit = QLineEdit("")
        self.qt_path_destination_edit = qt_path_destination_edit
        qt_path_destination_button = QPushButton("Get")
        qt_path_destination_button.setToolTip('Select directory')
        qt_path_destination_button.clicked.connect(self.on_click_get_destination_dir)
        qt_lay_path_destination.addWidget(qt_path_destination_label)
        qt_lay_path_destination.addWidget(qt_path_destination_edit)
        qt_lay_path_destination.addWidget(qt_path_destination_button)

        """  ADD PATHS  (SRC DEST)  """
        qt_lay_paths.addLayout(qt_lay_path_source)
        # qt_lay_paths.addSpacerItem(QSpacerItem(20,20))
        qt_lay_paths.addLayout(qt_lay_path_destination)


        qt_lay_buttons = QHBoxLayout()
        qt_info_button = QPushButton("Info")
        qt_info_button.clicked.connect(self.on_click_info)
        qt_check_button = QPushButton("Check")
        qt_check_button.clicked.connect(self.on_click_check)
        qt_install_button = QPushButton("Install")
        qt_install_button.clicked.connect(self.on_click_install)


        qt_lay_buttons.addWidget(qt_info_button)
        qt_lay_buttons.addWidget(qt_check_button)
        qt_lay_buttons.addWidget(qt_install_button)

        """  ADD TO CENTRAL  """
        #qt_lay_central.addLayout(self.animated_bar.qt_lay_animated_bar)
        qt_lay_central.addWidget(self.animated_bar)
        # qt_lay_central.addLayout(qt_lay_paths)
        qt_lay_central.addWidget(qt_gbox_paths)
        qt_lay_central.addLayout(qt_lay_buttons)
        self.setCentralWidget(qt_central_widget)
    def on_click_get_source_dir(self):
        self.comfun.get_dialog_directory(self.qt_path_source_edit, QFileDialog, dir_separator=self.dir_separator)
    def on_click_get_destination_dir(self):
        self.comfun.get_dialog_directory(self.qt_path_destination_edit, QFileDialog, dir_separator=self.dir_separator)

    def on_click_info(self):
        self.load_anim()
        self.play_anim()

    def on_click_check(self):
        pass

    def on_click_install(self):
        self.check()
        self.install()

    def load_anim(self, buffor_end = 100):
        
        anim_file = os.path.dirname(os.path.abspath(__file__)) + self.dir_separator + "anim.dat"
        
        
        print " anim_file  ", anim_file
        if self.comfun.file_exists(anim_file):
            anim_data = self.comfun.load_from_file(anim_file)
            
            # print "loaded " , self.animated_bar.canvas[0], self.animated_bar.canvas[1]
            # buffor_end = self.animated_bar.canvas[0]*self.animated_bar.canvas[1]
            anim_data += anim_file+"  ".join(["!" for i in range(0, buffor_end )])
            
            self.animated_bar.load_anim(anim_data)
            
    def play_anim(self):
        self.animated_bar.set_anim_format(4,18,200,double=False, pix_size=2, pix_offset=3)
        self.animated_bar.play_anim()


    def check(self):
        # TODO
        pass

    def install(self):
        # TODO
        pass

if __name__ == "__main__":
    if env_maya:
        main_window = InstallerWindow(400, 200)
        main_window.show()
    else:
        app = QApplication([])
        main_window = InstallerWindow()
        main_window.show()
        app.exec_()

    print ("env_maya", env_maya)
