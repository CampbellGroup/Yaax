import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
import pandas as pd
from editor import*


class ParameterVault(qtw.QWidget):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.x = Editor()

        #The Text Boxes
        self.path = qtw.QLineEdit()
        self.loc = qtw.QLineEdit()
        self.att = qtw.QLineEdit()
        self.val = qtw.QLineEdit()

         # Create textbox
        self.textbox = qtw.QTextEdit(self)
        self.textbox.move(35, 135)
        self.textbox.resize(280,500)

        # Create textbox
        self.atttextbox = qtw.QTextEdit(self)
        self.atttextbox.move(400, 135)
        self.atttextbox.resize(280,500)
        
        #THE BUTTONS
        self.sub0 = qtw.QPushButton('Submit Path')
        self.sub1 = qtw.QPushButton('Submit Group Path')
        self.sub2 = qtw.QPushButton('Submit Attribute and Value')
        self.sub3 = qtw.QPushButton('Show Attributes and Values')

        grandlayout = qtw.QGridLayout()
        
        #Input Widgets
        in_widgets = qtw.QWidget()
        in_widgets.setLayout(qtw.QFormLayout())
        layout0 = in_widgets.layout()
        layout0.addRow('Path', self.path)
        layout0.addRow('Group Path', self.loc)
        layout0.addRow('Attribute', self.att)
        layout0.addRow('Value', self.val)

        buttons = qtw.QWidget()
        buttons.setLayout(qtw.QFormLayout())
        layoutb = buttons.layout()
        layoutb.addRow(self.sub0)
        layoutb.addRow(self.sub1)
        layoutb.addRow(self.sub2)
        layoutb.addRow(self.sub3)
        
       
        grandlayout.addWidget(in_widgets, 0,0)
        grandlayout.addWidget(buttons, 0,1)

        self.setLayout(grandlayout)

        #SENDS THE SIGNAL TO UPDATE THE FILE
        self.sub0.clicked.connect(self.subpath)
        self.sub1.clicked.connect(self.subgroup)
        self.sub2.clicked.connect(self.subatt)
        self.sub3.clicked.connect(self.subshow)


        self.show()
    

    #EACH SUBMITTED FUNCTION WILLL UPDATE THE TEMP FILE AND THEN RUN THE ARTIQ CODE
    def subpath(self):
        self.x.pathchecker(self.path.text())
        direct = self.x.display(self.path.text())
        y_str = ''
        for y in direct:
            y_str += y + '\n'
        
        self.textbox.setText("The directories are: \n" + y_str)    
        pass

    def subgroup(self):
        self.x.write_att(self.path.text(),self.loc.text())
        self.subpath()
        pass

       
    def subatt(self):
        self.x.write_att(self.path.text(), self.loc.text(), self.att.text(),self.val.text())
        pass

    def subshow(self):
        k,v = self.x.attributecollector(self.path.text(),self.loc.text())

        y_str = ''
        x_str = ''
        att_str = ''
        i = 0
        
        for y in k:
            y_str += y + ': ' + str(v[i]) + '\n'
            i += 1

        att_str = y_str
        self.atttextbox.setText("The attributes and values are: \n" + att_str) 

        pass

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = ParameterVault()
    sys.exit(app.exec_())


