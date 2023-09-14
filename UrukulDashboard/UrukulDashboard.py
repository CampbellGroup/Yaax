import sys
import subprocess
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg
from datamanager import DataManager
import pandas as pd

class UrukulDashboard(qtw.QWidget,DataManager):


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #Sets up the defaults
        self.u0 = self.setdefault(0) 
        self.u1 = self.setdefault(1)
        self.u2 = self.setdefault(2)
        self.u3 = self.setdefault(3)

        #U0
        self.u0c0f = qtw.QLineEdit()
        self.u0c1f = qtw.QLineEdit()
        self.u0c2f = qtw.QLineEdit()
        self.u0c3f = qtw.QLineEdit()
        self.u0c0a = qtw.QLineEdit()
        self.u0c1a = qtw.QLineEdit()
        self.u0c2a = qtw.QLineEdit()
        self.u0c3a = qtw.QLineEdit()
        self.u0c0at = qtw.QLineEdit()
        self.u0c1at = qtw.QLineEdit()
        self.u0c2at = qtw.QLineEdit()
        self.u0c3at = qtw.QLineEdit()

        #U1
        self.u1c0f = qtw.QLineEdit()
        self.u1c1f = qtw.QLineEdit()
        self.u1c2f = qtw.QLineEdit()
        self.u1c3f = qtw.QLineEdit()
        self.u1c0a = qtw.QLineEdit()
        self.u1c1a = qtw.QLineEdit()
        self.u1c2a = qtw.QLineEdit()
        self.u1c3a = qtw.QLineEdit()
        self.u1c0at = qtw.QLineEdit()
        self.u1c1at = qtw.QLineEdit()
        self.u1c2at = qtw.QLineEdit()
        self.u1c3at = qtw.QLineEdit()

        #U2
        self.u2c0f = qtw.QLineEdit()
        self.u2c1f = qtw.QLineEdit()
        self.u2c2f = qtw.QLineEdit()
        self.u2c3f = qtw.QLineEdit()
        self.u2c0a = qtw.QLineEdit()
        self.u2c1a = qtw.QLineEdit()
        self.u2c2a = qtw.QLineEdit()
        self.u2c3a = qtw.QLineEdit()
        self.u2c0at = qtw.QLineEdit()
        self.u2c1at = qtw.QLineEdit()
        self.u2c2at = qtw.QLineEdit()
        self.u2c3at = qtw.QLineEdit()

        #U3
        self.u3c0f = qtw.QLineEdit()
        self.u3c1f = qtw.QLineEdit()
        self.u3c2f = qtw.QLineEdit()
        self.u3c3f = qtw.QLineEdit()
        self.u3c0a = qtw.QLineEdit()
        self.u3c1a = qtw.QLineEdit()
        self.u3c2a = qtw.QLineEdit()
        self.u3c3a = qtw.QLineEdit()
        self.u3c0at = qtw.QLineEdit()
        self.u3c1at = qtw.QLineEdit()
        self.u3c2at = qtw.QLineEdit()
        self.u3c3at = qtw.QLineEdit()

        #Prefill all of the textboxes
        self.prefill()
        
        #THE BUTTONS
        self.sub0 = qtw.QPushButton('Submit')
        self.sub1 = qtw.QPushButton('Submit')
        self.sub2 = qtw.QPushButton('Submit')
        self.sub3 = qtw.QPushButton('Submit')
        self.stop0 = qtw.QPushButton('Stop U0')
        self.stop1 = qtw.QPushButton('Stop U1')
        self.stop2 = qtw.QPushButton('Stop U3')
        self.stop3 = qtw.QPushButton('Stop U4')

        grandlayout = qtw.QGridLayout()
        
        #U0 Widget
        u0_widget = qtw.QWidget()
        u0_widget.setLayout(qtw.QFormLayout())
        layout0 = u0_widget.layout()
        layout0.addRow('u0c0freq', self.u0c0f)
        layout0.addRow('u0c0amp', self.u0c0a)
        layout0.addRow('u0c0att', self.u0c0at)

        layout0.addRow('u0c1freq', self.u0c1f)
        layout0.addRow('u0c1amp', self.u0c1a)
        layout0.addRow('u0c1att', self.u0c1at)

        layout0.addRow('u0c2freq', self.u0c2f)
        layout0.addRow('u0c2amp', self.u0c2a)
        layout0.addRow('u0c2att', self.u0c2at)

        layout0.addRow('u0c3freq', self.u0c3f)
        layout0.addRow('u0c3amp', self.u0c3a)
        layout0.addRow('u0c3att', self.u0c3at)

        button_widget0 = qtw.QWidget()
        button_widget0.setLayout(qtw.QVBoxLayout())
        button_widget0.layout().addWidget(self.sub0)
        button_widget0.layout().addWidget(self.stop0)
        layout0.addRow('', button_widget0)

        #U1 Widget
        u1_widget = qtw.QWidget()
        u1_widget.setLayout(qtw.QFormLayout())
        layout1 = u1_widget.layout()
        layout1.addRow('935AOMfeq', self.u1c0f)
        layout1.addRow('935AOMamp', self.u1c0a)
        layout1.addRow('935AOMatt', self.u1c0at)

        layout1.addRow('u1c1freq', self.u1c1f)
        layout1.addRow('u1c1amp', self.u1c1a)
        layout1.addRow('u1c1att', self.u1c1at)

        layout1.addRow('u1c2freq', self.u1c2f)
        layout1.addRow('u1c2amp', self.u1c2a)
        layout1.addRow('u1c2att', self.u1c2at)

        layout1.addRow('u1c3freq', self.u1c3f)
        layout1.addRow('u1c3amp', self.u1c3a)
        layout1.addRow('u1c3att', self.u1c3at)

        button_widget1 = qtw.QWidget()
        button_widget1.setLayout(qtw.QVBoxLayout())
        button_widget1.layout().addWidget(self.sub1)
        button_widget1.layout().addWidget(self.stop1)
        layout1.addRow('', button_widget1)

        #U2 Widget
        u2_widget = qtw.QWidget()
        u2_widget.setLayout(qtw.QFormLayout())
        layout2 = u2_widget.layout()
        layout2.addRow('u2c0freq', self.u2c0f)
        layout2.addRow('u2c0amp', self.u2c0a)
        layout2.addRow('u2c0att', self.u2c0at)

        layout2.addRow('u2c1freq', self.u2c1f)
        layout2.addRow('u2c1amp', self.u2c1a)
        layout2.addRow('u2c1att', self.u2c1at)

        layout2.addRow('u2c2freq', self.u2c2f)
        layout2.addRow('u2c2amp', self.u2c2a)
        layout2.addRow('u2c2att', self.u2c2at)

        layout2.addRow('u2c3freq', self.u2c3f)
        layout2.addRow('u2c3amp', self.u2c3a)
        layout2.addRow('u2c3att', self.u2c3at)
        
        button_widget2 = qtw.QWidget()
        button_widget2.setLayout(qtw.QVBoxLayout())
        button_widget2.layout().addWidget(self.sub2)
        button_widget2.layout().addWidget(self.stop2)
        layout2.addRow('', button_widget2)

        #U3 Widget
        u3_widget = qtw.QWidget()
        u3_widget.setLayout(qtw.QFormLayout())
        layout3 = u3_widget.layout()
        layout3.addRow('u3c0freq', self.u3c0f)
        layout3.addRow('u3c0amp', self.u3c0a)
        layout3.addRow('u3c0att', self.u3c0at)

        layout3.addRow('u3c1freq', self.u3c1f)
        layout3.addRow('u3c1amp', self.u3c1a)
        layout3.addRow('u3c1att', self.u3c1at)

        layout3.addRow('u3c2freq', self.u3c2f)
        layout3.addRow('u3c2amp', self.u3c2a)
        layout3.addRow('u3c2att', self.u3c2at)

        layout3.addRow('u3c3freq', self.u3c3f)
        layout3.addRow('u3c3amp', self.u3c3a)
        layout3.addRow('u3c3att', self.u3c3at)
        
        button_widget3 = qtw.QWidget()
        button_widget3.setLayout(qtw.QVBoxLayout())
        button_widget3.layout().addWidget(self.sub3)
        button_widget3.layout().addWidget(self.stop3)
        layout3.addRow('', button_widget3)

        grandlayout.addWidget(u0_widget, 0,0)
        grandlayout.addWidget(u1_widget, 0,1)
        grandlayout.addWidget(u2_widget, 0,2)
        grandlayout.addWidget(u3_widget, 0,3)

        self.setLayout(grandlayout)

        #SENDS THE SIGNAL TO UPDATE THE FILE
        self.sub0.clicked.connect(self.submitted0)
        self.sub1.clicked.connect(self.submitted1)
        self.sub2.clicked.connect(self.submitted2)
        self.sub3.clicked.connect(self.submitted3)

        #SENDS THE SIGNAL TO STOP ALL THE URUKULS
        self.stop0.clicked.connect(self.stopu0)
        self.stop1.clicked.connect(self.stopu1)
        self.stop2.clicked.connect(self.stopu2)
        self.stop3.clicked.connect(self.stopu3)


        self.show()
    

    #STOP THE URUKULS
    def stopu0(self):
        subprocess.Popen("cmd /k call uk0_stop.cmd")

    def stopu1(self):
        print("here")
        subprocess.Popen("cmd /k call uk1_stop.cmd")

    def stopu2(self):
        subprocess.Popen("cmd /k call uk2_stop.cmd")
    
    def stopu3(self):
        subprocess.Popen("cmd /k call uk3_stop.cmd")

    #EACH SUBMITTED FUNCTION WILLL UPDATE THE TEMP FILE AND THEN RUN THE ARTIQ CODE
    def submitted0(self):
        a = [self.u0c0f.text(),self.u0c1f.text(),self.u0c2f.text(),self.u0c3f.text(),
             self.u0c0a.text(),self.u0c1a.text(),self.u0c2a.text(),self.u0c3a.text(),
             self.u0c0at.text(),self.u0c1at.text(),self.u0c2at.text(),self.u0c3at.text()]
        
        for i in range(12):
            if a[i] == "" or float(a[i]) < 0 : 
                a[i] = self.u0[i]
            if float(a[i]) != self.u0[i]:
                self.u0[i] = float(a[i])
        
        #Update the temp file
        self.collector(self.u0,0)
        
        subprocess.Popen("cmd /k call uk0.cmd")

        #self.test()

    def submitted1(self):
        b = [self.u1c0f.text(),self.u1c1f.text(),self.u1c2f.text(),self.u1c3f.text(),
             self.u1c0a.text(),self.u1c1a.text(),self.u1c2a.text(),self.u1c3a.text(),
             self.u1c0at.text(),self.u1c1at.text(),self.u1c2at.text(),self.u1c3at.text()]
        
        for i in range(12):
            if b[i] == "" or float(b[i]) < 0 : 
                b[i] = self.u1[i]
            if float(b[i]) != self.u1[i]:
                self.u1[i] = float(b[i])

        #Update the temp file
        self.collector(self.u1,1)

        subprocess.Popen("cmd /k call uk1.cmd")
        #self.test()
    
    def submitted2(self):
        c = [self.u2c0f.text(),self.u2c1f.text(),self.u2c2f.text(),self.u2c3f.text(),
             self.u2c0a.text(),self.u2c1a.text(),self.u2c2a.text(),self.u2c3a.text(),
             self.u2c0at.text(),self.u2c1at.text(),self.u2c2at.text(),self.u2c3at.text()]
        
        for i in range(12):
            if c[i] == "" or float(c[i]) < 0 : 
                c[i] = self.u2[i]
            if float(c[i]) != self.u2[i]:
                self.u2[i] = float(c[i])
        
        #Update the temp file
        self.collector(self.u2,2)

        subprocess.Popen("cmd /k call uk2.cmd")
        #self.test()

    def submitted3(self):
        d = [self.u3c0f.text(),self.u3c1f.text(),self.u3c2f.text(),self.u3c3f.text(),
             self.u3c0a.text(),self.u3c1a.text(),self.u3c2a.text(),self.u3c3a.text(),
             self.u3c0at.text(),self.u3c1at.text(),self.u3c2at.text(),self.u3c3at.text()]
        
        for i in range(12):
            if d[i] == "" or float(d[i]) < 0 : 
                d[i] = self.u3[i]
            if float(d[i]) != self.u3[i]:
                self.u3[i] = float(d[i]) 
        
        #Update the temp file
        self.collector(self.u3,3)

        subprocess.Popen("cmd /k call uk3.cmd")
        #self.test()

    #Prefill with defaults
    def prefill(self):
        self.u0c0f.setText(str(self.u0[0]))
        self.u0c1f.setText(str(self.u0[1]))
        self.u0c2f.setText(str(self.u0[2]))
        self.u0c3f.setText(str(self.u0[3]))
        self.u0c0a.setText(str(self.u0[4]))
        self.u0c1a.setText(str(self.u0[5]))
        self.u0c2a.setText(str(self.u0[6]))
        self.u0c3a.setText(str(self.u0[7]))
        self.u0c0at.setText(str(self.u0[8]))
        self.u0c1at.setText(str(self.u0[9]))
        self.u0c2at.setText(str(self.u0[10]))
        self.u0c3at.setText(str(self.u0[11]))

        #U1
        self.u1c0f.setText(str(self.u1[0]))
        self.u1c1f.setText(str(self.u1[1]))
        self.u1c2f.setText(str(self.u1[2]))
        self.u1c3f.setText(str(self.u1[3]))
        self.u1c0a.setText(str(self.u1[4]))
        self.u1c1a.setText(str(self.u1[5]))
        self.u1c2a.setText(str(self.u1[6]))
        self.u1c3a.setText(str(self.u1[7]))
        self.u1c0at.setText(str(self.u1[8]))
        self.u1c1at.setText(str(self.u1[9]))
        self.u1c2at.setText(str(self.u1[10]))
        self.u1c3at.setText(str(self.u1[11]))

        #U2
        self.u2c0f.setText(str(self.u2[0]))
        self.u2c1f.setText(str(self.u2[1]))
        self.u2c2f.setText(str(self.u2[2]))
        self.u2c3f.setText(str(self.u2[3]))
        self.u2c0a.setText(str(self.u2[4]))
        self.u2c1a.setText(str(self.u2[5]))
        self.u2c2a.setText(str(self.u2[6]))
        self.u2c3a.setText(str(self.u2[7]))
        self.u2c0at.setText(str(self.u2[8]))
        self.u2c1at.setText(str(self.u2[9]))
        self.u2c2at.setText(str(self.u2[10]))
        self.u2c3at.setText(str(self.u2[11]))

        #U3
        self.u3c0f.setText(str(self.u3[0]))
        self.u3c1f.setText(str(self.u3[1]))
        self.u3c2f.setText(str(self.u3[2]))
        self.u3c3f.setText(str(self.u3[3]))
        self.u3c0a.setText(str(self.u3[4]))
        self.u3c1a.setText(str(self.u3[5]))
        self.u3c2a.setText(str(self.u3[6]))
        self.u3c3a.setText(str(self.u3[7]))
        self.u3c0at.setText(str(self.u3[8]))
        self.u3c1at.setText(str(self.u3[9]))
        self.u3c2at.setText(str(self.u3[10]))
        self.u3c3at.setText(str(self.u3[11]))

    def test(self):
        print("here")
        print(self.u0)
        print(self.u1)
        print(self.u2)
        print(self.u3)
        pass


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    w = UrukulDashboard()
    sys.exit(app.exec_())


