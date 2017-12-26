#!/usr/bin/python2.7

import sys
import logging
from PyQt4 import QtGui, QtCore
import pandas as pd
import xlrd

logging.basicConfig(level=logging.CRITICAL,
                    format='[%(threadName)s] %(message)s',
) 

class Gui(QtGui.QMainWindow):
    
    def __init__(self):
        super(Gui, self).__init__()        
        self.wid = None
        self.table = None
        self.fname = ''
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

        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)                        

        openFile = QtGui.QAction(QtGui.QIcon('excel.png'), "&Open Excel File", self)
        openFile.setShortcut("Ctrl+F")
        openFile.setStatusTip('Open Excel file and map')
        openFile.triggered.connect(self.fileOpen)

        helpAction = QtGui.QAction("&Help", self)
        helpAction.setShortcut("Ctrl+H")
        helpAction.triggered.connect(self.helpMessage)        
        
        menubar = self.menuBar()
        f_menu = menubar.addMenu('&File')
        f_menu.addAction(exitAction)        
        f_menu.addAction(openFile)        

        h_menu = menubar.addMenu('&Help')
        h_menu.addAction(helpAction)        
        
        self.toolbar = self.addToolBar('Open Excel File')
        self.toolbar.addAction(openFile)
        
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
        btn.setToolTip('Select and Map an Excel file columns to OBX commands\n' \
                        'Click on the excel icon on the top left to select and excel file')
        btn.clicked.connect(self.setMapping)                

        qbtn = QtGui.QPushButton('Quit', self)
        qbtn.setToolTip('Exit applicaton')        
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

        
    def fileOpen(self):
        _file = QtGui.QFileDialog.getOpenFileName(self, 'Open File')
        fname = str(_file)
        logging.debug("opened " + fname)

        if not fname:
            pass
        elif 'xlsx' in fname:
            self.fname = fname
            _xfile = pd.read_excel(self.fname)
            self.xcolmns = _xfile.columns
            logging.debug("columns found : " + str(self.xcolmns))            
            self.popTable()

        else:
            self.helpMessage()

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
            self.table.horizontalHeader().setVisible(False)
            self.table.verticalHeader().setVisible(False)            
            
        self.table.setRowCount(len(self.xcolmns))
        self.table.setColumnCount(2)
        
        x = 0
        for e in eles:
            self.table.setCellWidget(x,0, e[0])
            self.table.setCellWidget(x,1, e[1])            
            x+=1            

        header = self.table.horizontalHeader()
        header.setResizeMode(0, QtGui.QHeaderView.Stretch)
            
    def setMapping(self):
        print self.fname
        if not self.fname:
            self.helpMessage()
        else:
            tab_map = []
            for row in range(0,self.table.rowCount()):
                c0 = str(self.table.cellWidget(row,0).text())
                c1 = str(self.table.cellWidget(row,1).currentText())
                tab_map.append((c0,c1))
                logging.debug(c0 + " " + c1)

            print tab_map

def main():
    app = QtGui.QApplication(sys.argv)
    ex = Gui()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
