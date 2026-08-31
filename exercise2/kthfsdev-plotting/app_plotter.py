import sys
import time

import numpy as np

from matplotlib.backends.backend_qtagg import FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.figure import Figure

class PlotterApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        main_layout = QtWidgets.QGridLayout(self._main)
        left_panel_layout = QtWidgets.QGridLayout()
        main_layout.addLayout(left_panel_layout,0,0,2,1)

        #Add Elements from the left panel
        input_lambda_function = QtWidgets.QLabel(
            "Input Lambda Function \n" \
            " λ(t) = A sin(2πft)")
        left_panel_layout.addWidget(input_lambda_function, 0,0)

        input_lambda_checkbox = QtWidgets.QCheckBox()
        left_panel_layout.addWidget(input_lambda_checkbox, 0,1)
        
        # Add modifiable parameters
        a_param_label = QtWidgets.QLabel("A")
        left_panel_layout.addWidget(a_param_label,1,0)

        a_param_entrybox= QtWidgets.QLineEdit()
        left_panel_layout.addWidget(a_param_entrybox,1,1)

        f_param_label = QtWidgets.QLabel("f")
        left_panel_layout.addWidget(f_param_label,2,0)
        
        f_param_entrybox= QtWidgets.QLineEdit()
        left_panel_layout.addWidget(f_param_entrybox,2,1)

        # Add output function label
        output_function = QtWidgets.QLabel(
                    "Output Function \n" \
                    " h(t) = Bπ exp(-λt)")
        left_panel_layout.addWidget(output_function, 3,0)

        output_function_checkbox = QtWidgets.QCheckBox()
        left_panel_layout.addWidget(output_function_checkbox, 3,1)

        # Add modifiable parameters
        b_param_label = QtWidgets.QLabel("B")
        left_panel_layout.addWidget(b_param_label,4,0)

        b_param_entrybox= QtWidgets.QLineEdit()
        left_panel_layout.addWidget(b_param_entrybox,4,1)

        
        
        
        # Add Dynamic Input Canvas
        dynamic__input_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        main_layout.addWidget(dynamic__input_canvas,0,1)
        #layout.addWidget(NavigationToolbar(dynamic__input_canvas, self))

        # Add Dynamic Output Canvas
        dynamic__output_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        main_layout.addWidget(dynamic__output_canvas,1,1)
        #layout.addWidget(NavigationToolbar(dynamic__output_canvas, self))

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