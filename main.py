import sys
from PyQt5.QtWidgets import (QMainWindow, QWidget, QHBoxLayout,
                             QLabel, QApplication, QPushButton,QVBoxLayout,QDesktopWidget,QLabel)
from PyQt5.QtGui import QIcon,QColor,QPalette
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

#创建一个matplotlib图形绘制类
class MyFigure(FigureCanvas):
    def __init__(self,width=5, height=4, dpi=100):
        #第一步：创建一个创建Figure
        self.fig = Figure(figsize=(8, 8), dpi=dpi)
        #第二步：在父类中激活Figure窗口
        super(MyFigure,self).__init__(self.fig) #此句必不可少，否则不能显示图形
        #第三步：创建一个子图，用于绘制图形用，111表示子图编号，如matlab的subplot(1,1,1)
        self.axes = self.fig.add_subplot(111)
        #plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['font.sans-serif'] = ['SimHei']

    def plotPie(self):
        data = {
            '天': (60, '#7199cf'),
            '地': (45, '#4fc4aa'),
            '人': (120, '#ffff10'),
        }
        cities = data.keys()
        values = [x[0] for x in data.values()]
        colors = [x[1] for x in data.values()]
        labels = ['{}:{}'.format(city, value) for city, value in zip(cities, values)]
        print(labels)
        # 设置饼图的凸出显示
        explode = [0, 0.1, 0]
        self.axes.pie(values, labels=labels, colors=colors, explode=explode, shadow=True)
        self.fig.suptitle("pie")

class main(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()
    def initUI(self):
        # 整体布局为水平布局
        self.upest = QHBoxLayout(self)
        self.setScrollArea()#左
        self.setPie()       #右
        self.setLayout(self.upest)

        #图标
        self.setIcon()

        #页面设置
        self.SetWindoww()


    def setScrollArea(self):
        self.scrollArea = QtWidgets.QScrollArea(self)
        self.upest.addWidget(self.scrollArea)
        self.upest.addStretch(0)
        self.scrollArea.resize(1000, 1000)
        self.scrollcontent = QWidget()
        self.setMinimumHeight(10)  ###important
        lay1 = QVBoxLayout(self)

        background_color = QColor(194, 216, 217)
        background_color.setNamedColor('#000000')
        palette = QPalette()
        palette.setColor(QPalette.Window, background_color)
        for i in range(5):
            temp_lay = QHBoxLayout(self)
            temp = QLabel('00:00~24:00', self)
            temp.setStyleSheet('background-color: rgb(194, 216, 217);font-size:80px;color:black')
            # temp.resize(500, 600)
            temp_lay.addWidget(temp)
            # temp.setAutoFillBackground(True)
            # temp.setPalette(palette)
            temp = QLabel(str(i) + '学习', self)
            temp.setStyleSheet('background-color: rgb(232, 234, 212);font-size:40px;color:black')
            temp.setAlignment(Qt.AlignRight)
            temp_lay.addWidget(temp)
            lay1.addLayout(temp_lay)

        self.scrollcontent.setLayout(lay1)
        self.scrollArea.setWidget(self.scrollcontent)

    def setPie(self):
        # temp = QLabel('null')
        # temp.resize(500, 500)
        self.F = MyFigure(width=3, height=2, dpi=100)
        self.F.plotPie()

        self.pie = QWidget()
        self.pie.setGeometry(QtCore.QRect(180, 10, 1100, 500))
        self.graphicview = QtWidgets.QGraphicsView(self.pie)
        graphicscene = QtWidgets.QGraphicsScene()
        graphicscene.addWidget(self.F)
        self.graphicview.setScene(graphicscene)
        self.graphicview.show()

        self.upest.addWidget(self.pie)

    def setIcon(self):
        self.setWindowIcon(QIcon('icon.png'))

    def SetWindoww(self):
        self.move(403, 36)
        self.setFixedSize(1200, 900)
        self.setWindowTitle('觅时')

    def center(self):
        qr = self.frameGeometry()
        # 获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        # 显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = main()
    sys.exit(app.exec_())