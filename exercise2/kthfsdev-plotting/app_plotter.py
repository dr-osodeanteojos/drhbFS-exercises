import sys
import time

import numpy as np

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.figure import Figure
from PyQt6.QtCore import Qt
from PyQt6 import QtGui

class PlotterApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        self.set_UI()

    def set_UI(self):
        # Declare main layout grid and add a left panel grid layout
        main_layout = QtWidgets.QGridLayout(self._main)
        left_panel_layout = QtWidgets.QGridLayout()
        #left_panel_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        main_layout.addLayout(left_panel_layout,0,0,8,1)

        #Add Elements from the left panel
        # Add app header
        header_label = QtWidgets.QLabel("FStudent KTH")
        left_panel_layout.addWidget(header_label, 0,0,1,2)

        # Add spacer
        verticalSpacer1 = QtWidgets.QSpacerItem(5, 5, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding) 
        left_panel_layout.addItem(verticalSpacer1,1,1,1,2)
        

        # Add lambdafunction header
        input_lambda_function = QtWidgets.QLabel(
            "Input Lambda Function \n" \
            " λ(t) = A sin(2πft)")
        left_panel_layout.addWidget(input_lambda_function, 2,0)

        input_lambda_checkbox = QtWidgets.QCheckBox()
        left_panel_layout.addWidget(input_lambda_checkbox, 2,1)
        
        # Add modifiable parameters
        a_param_label = QtWidgets.QLabel("A")
        left_panel_layout.addWidget(a_param_label,3,0)

        a_param_entrybox= QtWidgets.QLineEdit()
        left_panel_layout.addWidget(a_param_entrybox,3,1)

        f_param_label = QtWidgets.QLabel("f")
        left_panel_layout.addWidget(f_param_label,4,0)
        
        f_param_entrybox= QtWidgets.QLineEdit()
        left_panel_layout.addWidget(f_param_entrybox,4,1)

        # Add spacer element
        verticalSpacer2 = QtWidgets.QSpacerItem(5, 5, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding) 
        left_panel_layout.addItem(verticalSpacer2,5,1,1,2)


        # Add output function label
        output_function = QtWidgets.QLabel(
                    "Output Function \n" \
                    " h(t) = Bπ exp(-λ(t))")
        left_panel_layout.addWidget(output_function, 6,0)

        output_function_checkbox = QtWidgets.QCheckBox()
        left_panel_layout.addWidget(output_function_checkbox, 6,1)

        # Add modifiable parameters
        b_param_label = QtWidgets.QLabel("B")
        left_panel_layout.addWidget(b_param_label,7,0)

        b_param_entrybox= QtWidgets.QLineEdit()
        left_panel_layout.addWidget(b_param_entrybox,7,1)

        #Add vertical spacer
        verticalSpacer3 = QtWidgets.QSpacerItem(5, 5, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding) 
        left_panel_layout.addItem(verticalSpacer3,8,1,1,2)

        
        # Add Start/Stop button
        self.start_stop_button = QtWidgets.QPushButton("Start/Stop")
        left_panel_layout.addWidget(self.start_stop_button,9,0)

        # Add reset button
        self.reset_button = QtWidgets.QPushButton("Reset")
        left_panel_layout.addWidget(self.reset_button,9,1)
        

        # Add rest of the elements
        # Add experiment name label
        experiment_name_label = QtWidgets.QLabel("Experiment Name:")
        main_layout.addWidget(experiment_name_label,0,1)

        # Add experiment name lineEdit
        self.experiment_name_entrybox = QtWidgets.QLineEdit()
        main_layout.addWidget(self.experiment_name_entrybox,0,2)

        # Add Grid button
        self.grid_button = QtWidgets.QPushButton('Grid Toggle')
        main_layout.addWidget(self.grid_button,0,3)

        # Add custom export button
        self.export_button = QtWidgets.QPushButton('export')
        main_layout.addWidget(self.export_button,0,4)

        # Add Dynamic Input Canvas
        dynamic__input_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        main_layout.addWidget(dynamic__input_canvas,1,1,1,4)
        main_layout.addWidget(NavigationToolbar(dynamic__input_canvas, self),2,1,1,4)

        # Add Dynamic Output Canvas
        dynamic__output_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        main_layout.addWidget(dynamic__output_canvas,3,1,1,4)
        main_layout.addWidget(NavigationToolbar(dynamic__output_canvas, self),4,1,1,4)



        self._dynamic_ax = dynamic__input_canvas.figure.subplots()
        # Set up a Line2D.
        self.xdata = np.linspace(0, 10, 101)
        self.update_ydata()
        self._line, = self._dynamic_ax.plot(self.xdata, self.ydata)
        
    def update_ydata(self):
        # Shift the sinusoid as a function of time.
        self.ydata = np.sin(self.xdata + time.time())

    def update_canvas(self):
        self._line.set_data(self.xdata, self.ydata)
        # It should be safe to use the synchronous draw() method for most drawing
        # frequencies, but it is safer to use draw_idle().
        self._line.figure.canvas.draw_idle()    


if __name__ == '__main__':
    
    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)

    app = PlotterApp()
    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec()