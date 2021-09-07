from PyQt5 import QtCore, QtGui, QtWidgets
import example_ui as ui

class Main(QtWidgets.QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
         super().__init__()
         self.setupUi(self)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
