# -*- coding: utf-8 -*-
from sys import argv, exit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication,QLabel,QWidget,QGridLayout, QPushButton, QRadioButton, QButtonGroup, QComboBox,
                             QLineEdit, QInputDialog)

class statistic(QWidget):
    def __init__(self):
        super(statistic, self).__init__()
        self.init_ui()
        self.show()

    def init_ui(self):#窗口初始化，组件布局
        self.setFixedSize(700, 400)
        self.setWindowFlags(Qt.WindowMinimizeButtonHint)
        self.setWindowTitle('觅时')
        self.setWindowIcon(QIcon('./images/others/icon.png'))
        self.setWindowModality(Qt.ApplicationModal)
        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.time_set()
        self.label_set()

        self.okBtn = QPushButton("确定")
        self.cancelBtn = QPushButton("取消")
        self.grid.addWidget(self.okBtn,5,1)
        self.grid.addWidget(self.cancelBtn,5,2)
        self.state=0
        self.okBtn.clicked.connect(self.closeOk)
        self.cancelBtn.clicked.connect(self.closeCancel)

        self.setLayout(self.grid)

    def closeOk(self):
        self.insert_newlabel(self.new_label.text())
        self.state=1
        self.close()

    def closeCancel(self):
        self.state=2
        self.close()

    def time_set(self):
        self.label = QLabel("计时方式：", self)
        self.upButton = QRadioButton("自由计时")
        self.fallButton = QRadioButton("倒计时")
        self.time_button=0

        self.grid.addWidget(self.label,1,0)
        self.grid.addWidget(self.upButton,1,1)
        self.grid.addWidget(self.fallButton,1,2)

        self.buttonGroup_2 = QButtonGroup()
        self.buttonGroup_2.addButton(self.upButton)
        self.buttonGroup_2.addButton(self.fallButton)

        self.upButton.setChecked(True)

        self.hour_time = QComboBox()
        self.hour_time.addItem("0")
        self.hour_time.addItem("1")
        self.hour_time.addItems(["2", "3", "4","5","6","7","8","9","10","11","12"])
        self.grid.addWidget(self.hour_time, 1, 3)
        self.hour_time.setVisible(False)
        self.label_hour=QLabel("时",self)
        self.grid.addWidget(self.label_hour,1,4)
        self.label_hour.setVisible(False)

        self.minite_time = QComboBox()
        self.minite_time.addItem("0")
        self.minite_time.addItem("1")
        self.minite_time.addItems(["2", "3", "4","5","6","7","8","9","10","11","12", "13", "14","15","16","17","18","19","20","21","22", "23", "24","25","26","27","28","29","30","31","32", "33", "34","35","36","37","38","39","40","41","42", "43", "44","45","46","47","48","49","50","51","52", "53", "54","55","56","57","58","59"])
        self.grid.addWidget(self.minite_time, 1, 5)
        self.minite_time.setVisible(False)
        self.label_minite=QLabel("分",self)
        self.grid.addWidget(self.label_minite,1,6)
        self.label_minite.setVisible(False)

        self.second_time = QComboBox()
        self.second_time.addItem("0")
        self.second_time.addItem("1")
        self.second_time.addItems(["2", "3", "4","5","6","7","8","9","10","11","12", "13", "14","15","16","17","18","19","20","21","22", "23", "24","25","26","27","28","29","30","31","32", "33", "34","35","36","37","38","39","40","41","42", "43", "44","45","46","47","48","49","50","51","52", "53", "54","55","56","57","58","59"])
        self.grid.addWidget(self.second_time, 1, 7)
        self.second_time.setVisible(False)
        self.label_second=QLabel("秒",self)
        self.grid.addWidget(self.label_second,1,8)
        self.label_second.setVisible(False)

        self.fallButton.toggled.connect(lambda :self.fall_time(self.fallButton))

    def fall_time(self,fallButton):
        if fallButton.isChecked()==True:
            self.hour_time.setVisible(True)
            self.label_hour.setVisible(True)
            self.minite_time.setVisible(True)
            self.label_minite.setVisible(True)
            self.second_time.setVisible(True)
            self.label_second.setVisible(True)
            self.time_button=1
            self.hour_time_return=0
            self.minute_time_return = 0
            self.second_time_return = 0
            self.hour_time.currentIndexChanged.connect(self.selectionchange_hour)
            self.minite_time.currentIndexChanged.connect(self.selectionchange_minite)
            self.second_time.currentIndexChanged.connect(self.selectionchange_second)
        else:
            self.hour_time.setVisible(False)
            self.label_hour.setVisible(False)
            self.minite_time.setVisible(False)
            self.label_minite.setVisible(False)
            self.second_time.setVisible(False)
            self.label_second.setVisible(False)
            self.time_button=0

    def label_set(self):
        self.label2 = QLabel("标签名称：", self)

        self.buttonGroup_1 = QButtonGroup()

        self.old = QRadioButton("选择已有标签")
        self.old_label = QComboBox()
        # self.old_label.addItem("默认")
        # self.old_label.addItem("学习")
        #self.load_oldlabels() #zd

        self.old_label.setVisible(True)
        self.grid.addWidget(self.label2, 2, 0)
        self.grid.addWidget(self.old,2,1)
        self.grid.addWidget(self.old_label,2,2)

        self.old.toggled.connect(self.old_labelcheck)

        self.label_hide=QLabel("删除标签:",self)
        self.hide=QPushButton("确认")
        self.hide_label=QComboBox()
        self.load_oldlabels() # old_label and hide_label
        self.grid.addWidget(self.label_hide,4,0)
        self.grid.addWidget(self.hide,4,2)
        self.grid.addWidget(self.hide_label,4,1)

        self.new = QRadioButton("新增标签")
        self.new_label = QLabel('',self) #zd
        self.space=QLineEdit(self)
        self.space.setReadOnly(True)
        self.space.setStyleSheet("background:transparent;border-width:0;border-style:outset");
        self.new.toggled.connect(self.new_labelcheck)
        self.grid.addWidget(self.new,3,1)
        self.grid.addWidget(self.space,3,3)
        self.grid.addWidget(self.new_label,3,2)

        self.buttonGroup_1.addButton(self.old)
        self.buttonGroup_1.addButton(self.new)

        self.old.setChecked(True)

    def old_labelcheck(self):
        if self.old.isChecked():
            self.old_label.setVisible(True)
            self.new_label.setVisible(False)
            self.label_return = "默认"
            self.old_label.currentIndexChanged.connect(self.selectionchange)

    def new_labelcheck(self):
        if self.new.isChecked():
            self.old_label.setVisible(False)
            label, ok = QInputDialog.getText(self, '新增标签','标签名')
            if ok and (len(label)!=0):
                self.new_label.setText(str(label))
            else:
                self.new_label.setText("默认")
            self.new_label.setVisible(True)
            self.label_return = "默认"
            self.label_return = self.new_label.text()

    def selectionchange(self):
        self.label_return = self.old_label.currentText()

    def selectionchange_hour(self):
        self.hour_time_return =self.hour_time.currentText()

    def selectionchange_minite(self):
        self.minute_time_return =self.minite_time.currentText()

    def selectionchange_second(self):
        self.second_time_return = self.second_time.currentText()

    #加载已有标签
    def load_oldlabels(self): #zd
        self.hide_label.addItem('')
        with open('./data/labels', 'rb') as f:
            self.labels_list = [x.decode('utf-8').strip() for x in f.readlines() if x.decode('utf-8').strip()]
            for x in self.labels_list:
                self.old_label.addItem(x)
                if x!='默认':
                    self.hide_label.addItem(x)
    #写入新标签
    def insert_newlabel(self, newlabel):
        if newlabel=='' or newlabel in self.labels_list:
            print('已经存在')
            return

        with open('./data/labels', 'a', encoding='utf-8') as f:
            f.write(newlabel+'\n')

# if __name__ == "__main__":
#     app = QApplication(argv)
#     w = statistic()
#     exit(app.exec_())