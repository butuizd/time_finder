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
import sip
import time

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
        explode = [0, 0, 0]
        self.axes.pie(values, labels=labels, colors=colors, explode=explode, shadow=True)
        self.fig.suptitle("pie")

class main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()
    def initUI(self):
        # 整体布局为水平布局
        self.centralWidget = QWidget(self)
        self.upest = QHBoxLayout()
        self.setScrollArea()#左
        self.setPie()       #右
        self.centralWidget.setLayout(self.upest)
        self.setCentralWidget(self.centralWidget)

        #图标
        self.setIcon()

        #页面设置
        self.SetWindoww()

        #设置菜单
        menu = self.menuBar()
        item = menu.addMenu('&日期选择')
        ac   = QtWidgets.QAction('&Exit', self)
        ac.triggered.connect(self.redraw)
        item.addAction(ac)

    def redraw(self):
        print(self.sender().text())
        print(self.lay1.children())
        self.scrollArea.removeItem(self.lay1)
        # self.lay1.addLayout(QHBoxLayout(self))
        # for i in self.lay1.children():
        #     print(i)
        #     break
        # self.lay1.removeItem(i)
        # sip.delete(i)
        # for i in self.lay1.children():
        #     self.lay1.removeItem(i)
        #     sip.delete(i)
        # print(self.lay1.children())
        QApplication.processEvents()
        time.sleep(1)

    def setScrollArea(self):
        self.scrollArea = QtWidgets.QScrollArea(self)
        self.upest.addWidget(self.scrollArea)
        self.scrollArea.resize(1000, 1000)
        self.scrollcontent = QWidget()
        self.setMinimumHeight(10)  ###important
        self.lay1 = QVBoxLayout(self)

        background_color = QColor(194, 216, 217)
        background_color.setNamedColor('#000000')
        palette = QPalette()
        palette.setColor(QPalette.Window, background_color)
        '''
               for i in range(2):
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
            # a = QWidget(self)
            # a.setLayout(temp_lay)
            # self.lay1.addChildWidget(a)
            self.lay1.addLayout(temp_lay) 
        '''
        for i in range(3):
            temp_lay = QHBoxLayout(self)
            temp = QLabel('00:00~24:00', self)
            temp.setStyleSheet('background-color: rgb(194, 216, 217);font-size:80px;color:black')
            # # temp.resize(500, 600)
            # temp_lay.addWidget(temp)
            # # temp.setAutoFillBackground(True)
            # # temp.setPalette(palette)
            # temp = QLabel(str(i) + '学习', self)
            # temp.setStyleSheet('background-color: rgb(232, 234, 212);font-size:40px;color:black')
            # temp.setAlignment(Qt.AlignRight)
            #temp_lay.addWidget(temp)
            self.lay1.addWidget(temp)


        self.scrollcontent.setLayout(self.lay1)
        self.scrollArea.setWidget(self.scrollcontent)

    def setPie(self):
        # temp = QLabel('null')
        # temp.resize(500, 500)
        self.F = MyFigure(width=3, height=2)
        self.F.plotPie()

        #self.pie = QWidget()
        #self.pie.setGeometry(QtCore.QRect(180, 10, 1100, 500))
        self.graphicview = QtWidgets.QGraphicsView()
        self.graphicview.horizontalScrollBar().setVisible(False)
        graphicscene = QtWidgets.QGraphicsScene()
        graphicscene.addWidget(self.F)

        print(self.graphicview.geometry())
        # scene是一个展示2D图形的场景，setSceneRect的效果是设置场景中可见的矩形范围
        # 参数a b c d; a是可见范围左上角坐标的横坐标 b是纵坐标； c是可见范围的横向距离，d是纵向距离
        graphicscene.setSceneRect(QtCore.QRectF(101, 300, 590, 100))
        self.graphicview.setScene(graphicscene)
        self.graphicview.show()

        self.upest.addWidget(self.graphicview)

    def setIcon(self):
        self.setWindowIcon(QIcon('icon.png'))

    def SetWindoww(self):
        self.move(403, 36)
        #self.resize(1200,900)
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