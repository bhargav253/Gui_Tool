#!/usr/bin/python2.7

import sys
import logging
from PyQt4 import QtGui, QtCore

logging.basicConfig(level=logging.DEBUG,
                    format='[%(threadName)s] %(message)s',
) 

class Example(QtGui.QMainWindow):
    
    def __init__(self):
        super(Example, self).__init__()        
        self.wid = None
        self.table = None
        self.xcolmns = ['Column1','Column2','Column3','...','...','ColumnN']
        self.hl7_rows = ['OBX1.1','OBX1.2','OBX1.3','OBX2.1','OBX2.2','OBX3']        

        self.initWindow()
        self.initMenu()        
        self.popTable()
        self.initPage()                
        self.runWindow()
        
    def initWindow(self):        
        logging.debug("initializing window") 

        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))

        self.wid = QtGui.QWidget(self)
        self.setCentralWidget(self.wid)
        
    def initMenu(self):
        logging.debug("initializing Menu/Tool/Status Bars") 

        exitAction = QtGui.QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)                        

        openFile = QtGui.QAction(QtGui.QIcon('web.png'), "&Open File", self)
        openFile.setShortcut("Ctrl+F")
        openFile.setStatusTip('Open Xcel file')
        openFile.triggered.connect(self.fileOpen)
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)        

        self.toolbar = self.addToolBar('Open File')
        self.toolbar.addAction(openFile)
        
        self.statusBar().showMessage('Ready')

        
    def initPage(self):        
        logging.debug("setting Page") 

        btn = QtGui.QPushButton('Create', self)
        btn.setToolTip('This is a <b>QPushButton</b> widget')
        #btn.resize(btn.sizeHint())
        #btn.move(50, 50)       

        qbtn = QtGui.QPushButton('Quit', self)
        qbtn.setToolTip('Click to exit applicaton')        
        #qbtn.resize(qbtn.sizeHint())
        #qbtn.move(150, 50)
        qbtn.clicked.connect(self.close)        

        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(btn)
        hbox.addWidget(qbtn)

        vbox = QtGui.QVBoxLayout()
        #vbox.addStretch(1)
        vbox.addWidget(self.table)
        vbox.addLayout(hbox)
        
        self.wid.setLayout(vbox)
        
    def popTable(self):
        eles = []
        
        for c in self.xcolmns:
            l = QtGui.QLabel(c)
            t = QtGui.QComboBox()
            t.addItems(self.hl7_rows)
            #t.completer().setCompletionMode(QtGui.QCompleter.PopupCompletion)
            eles.append((l,t))
            
        if not self.table:
            self.table = QtGui.QTableWidget()

        self.table.setRowCount(len(self.xcolmns))
        self.table.setColumnCount(2)
        
        x = 0
        for e in eles:
            self.table.setCellWidget(x,0, e[0])
            self.table.setCellWidget(x,1, e[1])            
            x+=1            
        
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
                                           "Are you sure to quit?", QtGui.QMessageBox.Yes |
                                           QtGui.QMessageBox.No, QtGui.QMessageBox.No)        
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()                                            
            
    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        logging.debug("frame size is " + str(qr) + "center point is " + str(cp)) 
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def fileOpen(self):
        _file = QtGui.QFileDialog.getOpenFileName(self, 'Open File')
        logging.debug("opened " + str(_file))

        self.xcolmns = ['obiwan','yoda','darthvader','luke']
        self.hl7_rows = ['KBX1.1','KBX1.2','KBX1.3','KBX2.1','KBX2.2','KBX3']
        self.popTable()
        
    def runWindow(self):
        self.resize(800, 800)
        self.center()
        self.setWindowTitle('Tool')
        self.show()

        
def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
