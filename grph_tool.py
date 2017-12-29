#!/usr/bin/python2.7

import random
import sys
import logging
from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.widgets import MultiCursor
from matplotlib.figure import Figure

logging.basicConfig(level=logging.CRITICAL,
                    format='[%(threadName)s] %(message)s',
) 

class Gui(QtGui.QMainWindow):
    
    def __init__(self):
        super(Gui, self).__init__()        
        self.wid = None

        self.initWindow()
        self.initGraph()
        self.initMenu()        
        self.initPage()                
        self.runWindow()
        
    def initWindow(self):        
        logging.debug("initializing window") 

        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))

        self.wid = QtGui.QWidget(self)
        self.setCentralWidget(self.wid)

    def initGraph(self):
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas,self)                
        
    def initMenu(self):
        logging.debug("initializing Menu/Tool/Status Bars") 

        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)                        

        helpAction = QtGui.QAction("&Help", self)
        helpAction.setShortcut("Ctrl+H")
        helpAction.triggered.connect(self.helpMessage)        
        
        menubar = self.menuBar()
        f_menu = menubar.addMenu('&File')
        f_menu.addAction(exitAction)        

        h_menu = menubar.addMenu('&Help')
        h_menu.addAction(helpAction)        
                
        self.statusBar().showMessage('Ready')

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        logging.debug("frame size is " + str(qr) + "center point is " + str(cp)) 
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def runWindow(self):
        self.resize(400, 800)
        self.center()
        self.setWindowTitle('Tool')
        self.setWindowIcon(QtGui.QIcon('tool.png'))
        self.show()

    def initPage(self):        
        logging.debug("setting Page") 

        btn = QtGui.QPushButton('Map', self)
        btn.clicked.connect(self.popGraph)                

        qbtn = QtGui.QPushButton('Quit', self)
        qbtn.setToolTip('Exit applicaton')        
        qbtn.clicked.connect(self.close)        

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(btn)
        hbox.addWidget(qbtn)

        vbox = QtGui.QVBoxLayout()
        #vbox.addStretch(1)
        vbox.addWidget(self.toolbar)
        vbox.addWidget(self.canvas)        
        vbox.addLayout(hbox)
        
        self.wid.setLayout(vbox)
                
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
                                           "Are you sure to quit?", QtGui.QMessageBox.Yes |
                                           QtGui.QMessageBox.No, QtGui.QMessageBox.No)        
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()                                            

    def helpMessage(self):
        help_msg = QtGui.QMessageBox.question(self, 'Select a valid file',
                                              'Please select an xlsx file by clicking on the excel icon ' \
                                              'on the top left and then start mapping', QtGui.QMessageBox.Ok)

        
    def popGraph(self):
        data = [random.random() for i in range(10)]
        a1 = self.figure.add_subplot(211)
        a2 = self.figure.add_subplot(212, sharex=a1)

        a1.clear()
        a2.clear()        
        
        a1.plot(data)
        a2.plot(data[::-1])

        multi = MultiCursor(self.figure.canvas,(a1,a2),color='r',horizOn=True,vertOn=True)

        def onclick(event):
            multi.onmove(event)
        self.canvas.mpl_connect('ggwp',onclick)
        
        self.canvas.draw()        
        
def main():
    app = QtGui.QApplication(sys.argv)
    ex = Gui()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
