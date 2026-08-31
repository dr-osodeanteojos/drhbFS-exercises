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

        # Declare initial parameter values for the functions λ(t), h(t)
        self.A = 5
        self.B = 3
        self.f = 1

        # Declare control flags
        self.start_stop_flag = 0      

        # Create UI elements
        self.set_UI()

        # Set initial values of the UI
        self.set_initial_values()

        # Set plot functions and timers
        self.set_plotting_functions()

    def set_plotting_functions(self):
        self.input_dynamic_ax = self.dynamic_input_canvas.figure.subplots()
        self.output_dynamic_ax = self.dynamic_output_canvas.figure.subplots()

        # Set up the xdata space
        self.xdata = np.linspace(0, 2*np.pi, 1001)
        self.update_functions()

        self.line_input, = self.input_dynamic_ax.plot(self.xdata, self.l_ydata)
        self.line_output, = self.output_dynamic_ax.plot(self.xdata, self.h_ydata)


        # Declare the timers that drive real-time update
        self.data_timer = self.dynamic_input_canvas.new_timer(1)
        self.data_timer.add_callback(self.update_functions)
        
        self.drawing_timer = self.dynamic_input_canvas.new_timer(20) #50Hz
        self.drawing_timer.add_callback(self.update_canvas)


    def set_initial_values(self):
        # Add initial parameters values to the corresponding line edits
        self.a_param_entrybox.setText(f"{self.A}")
        self.b_param_entrybox.setText(f"{self.B}")
        self.f_param_entrybox.setText(f"{self.f}")
    
        # Set checkboxes to true
        self.input_lambda_checkbox.setChecked(True)
        self.output_function_checkbox.setChecked(True)

        # Add dummy text for experiment
        self.experiment_name_entrybox.setText("Test - Hurtado")
                        
    def set_UI(self):
        # Set window title
        self.setWindowTitle("Graph Plotter")
        # Declare main widget of the app
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
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
        input_lambda_function_label = QtWidgets.QLabel(
            "Input Lambda Function \n" \
            " λ(t) = A sin(2πft)")
        left_panel_layout.addWidget(input_lambda_function_label, 2,0)

        self.input_lambda_checkbox = QtWidgets.QCheckBox()
        left_panel_layout.addWidget(self.input_lambda_checkbox, 2,1)
        
        # Add modifiable parameters
        a_param_label = QtWidgets.QLabel("A")
        left_panel_layout.addWidget(a_param_label,3,0)

        self.a_param_entrybox= QtWidgets.QLineEdit()
        left_panel_layout.addWidget(self.a_param_entrybox,3,1)

        f_param_label = QtWidgets.QLabel("f")
        left_panel_layout.addWidget(f_param_label,4,0)
        
        self.f_param_entrybox= QtWidgets.QLineEdit()
        left_panel_layout.addWidget(self.f_param_entrybox,4,1)

        # Add spacer element
        verticalSpacer2 = QtWidgets.QSpacerItem(5, 5, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding) 
        left_panel_layout.addItem(verticalSpacer2,5,1,1,2)


        # Add output function label
        output_function = QtWidgets.QLabel(
                    "Output Function \n" \
                    " h(t) = Bπ exp(-λ(t))")
        left_panel_layout.addWidget(output_function, 6,0)

        self.output_function_checkbox = QtWidgets.QCheckBox()
        left_panel_layout.addWidget(self.output_function_checkbox, 6,1)

        # Add modifiable parameters
        b_param_label = QtWidgets.QLabel("B")
        left_panel_layout.addWidget(b_param_label,7,0)

        self.b_param_entrybox= QtWidgets.QLineEdit()
        left_panel_layout.addWidget(self.b_param_entrybox,7,1)

        #Add vertical spacer
        verticalSpacer3 = QtWidgets.QSpacerItem(5, 5, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding) 
        left_panel_layout.addItem(verticalSpacer3,8,1,1,2)

        
        # Add Start/Stop button
        self.start_stop_button = QtWidgets.QPushButton("Start/Stop")
        left_panel_layout.addWidget(self.start_stop_button,9,0)
        self.start_stop_button.clicked.connect(self.start_stop)


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
        self.dynamic_input_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        main_layout.addWidget(self.dynamic_input_canvas,1,1,1,4)
        main_layout.addWidget(NavigationToolbar(self.dynamic_input_canvas, self),2,1,1,4)

        # Add Dynamic Output Canvas
        self.dynamic_output_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        main_layout.addWidget(self.dynamic_output_canvas,3,1,1,4)
        main_layout.addWidget(NavigationToolbar(self.dynamic_output_canvas, self),4,1,1,4)

    
    def update_functions(self):
        # Shift the lambda function as a function of time.
        self.l_ydata = self.A*np.sin(2*np.pi*self.f*self.xdata + time.time())
        # Update y data of h(t)
        self.h_ydata = self.B*np.pi*np.exp(self.l_ydata)

    def update_canvas(self):
        # Update data
        self.line_input.set_data(self.xdata, self.l_ydata)
        self.line_output.set_data(self.xdata, self.l_ydata)

        # Update canvas
        self.line_input.figure.canvas.draw_idle()
        self.line_output.figure.canvas.draw_idle()    

    def start_stop(self):
        self.start_stop_flag = not self.start_stop_flag
        if self.start_stop_flag:
            self.data_timer.start()
            self.drawing_timer.start()
        else:
            self.data_timer.stop()
            self.drawing_timer.stop()


if __name__ == '__main__':
    
    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)

    app = PlotterApp()
    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec()