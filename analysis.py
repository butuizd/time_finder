import sys
import os
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
import json

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

class analysis(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()

    def initUI(self):
        # 设置菜单并获取日期列表
        self.loadMenu()
        # 加载初始化数据
        self.load_initial_data()
        #设置提示信息字体
        ##
        # 整体布局为水平布局
        self.centralWidget = QWidget(self)
        self.upest = QHBoxLayout()
        self.setScrollArea()
        self.setPie()  # 右

        self.centralWidget.setLayout(self.upest)
        self.setCentralWidget(self.centralWidget)

        #图标
        self.setIcon()

        #页面设置
        self.SetWindoww()

    def loadMenu(self):
        #从数据库读取日期信息
        if not os.path.isfile('./data/date_list'):
            os.system('copy nul date_list')
            print('not exist')
        else:
            print('exists!')

        with open('./data/date_list','r') as f:
            self.date_list = [x.strip() for x in f.readlines()]

        print(self.date_list)
        #self.date_list = ['2019/5/16','2019/5/17']
        menu = self.menuBar()
        item = menu.addMenu('&日期选择')
        for i in self.date_list:
            ac   = QtWidgets.QAction(i,self)
            ac.triggered.connect(self.redraw)
            item.addAction(ac)

    def load_initial_data(self):
        def filter_date(date_list, date):
            return [x for x in date_list if x['phase'][0]==date]

        self.colors = ['#90ed7d','#f7a35c','#f15c80','#7199cf', '#4fc4aa', '#ffff10']
        #self.colors = ['#90ed7d', '#f7a35c', '#f15c80']
        if not self.date_list:
            self.initial_timeline = []
            self.initial_pie = {}
            self.date_list = ['没有任务记录~']
            return

        with open('./data/tasks','r') as f:
            tasks_to_show = filter_date([json.loads(x.strip('\n')) for x in f.readlines()], self.date_list[-1])

        print(tasks_to_show)
        #从数据库获取最新一天的数据
        # tasks_to_show = [
        #     {'title': '程设', 'phase': ('2019/5/17', '8:00', '10:50'), 'tags': '学习'},
        #     {'title': '打游戏', 'phase': ('2019/5/17', '1:30', '4:20'), 'tags': '娱乐'},
        #     {'title': '打篮球', 'phase': ('2019/5/17', '18:00', '19:15'), 'tags': '运动'}
        # ]
        self.initial_timeline = tasks_to_show
        #self.initial_timeline = []
        self.initial_pie = {x['tags']:self.time_len([x['phase'][1], x['phase'][2]]) for x in tasks_to_show}
        #self.initial_pie = []
        test = [
            {'title': '程设', 'phase': ('2019/5/17', '8:00', '10:50'), 'tags': '测试0'},
            {'title': '打游戏', 'phase': ('2019/5/17', '1:30', '4:20'), 'tags': '测试1'},
            {'title': '打篮球', 'phase': ('2019/5/17', '18:00', '19:15'), 'tags': '测试2'}
        ]

        #self.test = {x['tags']:self.time_len([x['phase'][1], x['phase'][2]]) for x in test}
        self.test = test

    def time_len(self, time_points):
        #计算两个字符串格式日期的时间间隔 按分钟计
        t1 = time_points[0].split(':')
        t2 = time_points[1].split(':')
        t1 = [int(x) for x in t1]
        t2 = [int(x) for x in t2]
        return 60*(t2[0]-1-t1[0]) + 60+t2[1]-t1[1]

    def time_transform(self, tbegin, tend):
        t1 = tbegin.split(':')
        t2 = tend.split(':')
        t1 = [int(x) for x in t1]
        t2 = [int(x) for x in t2]
        return t1[0]*60+t1[1], t2[0]*60+t2[1]

    def redraw(self):
        def filter_date(date_list, date):
            return [x for x in date_list if x['phase'][0]==date]

        date_to_show = self.sender().text()
        #从数据库提取指定日期的任务列表，每个元素是一个字典
        tasks_to_show = [
            {'title': '程设', 'phase': ('2019/5/17', '8:00', '10:20'), 'tags': '你好'},
            {'title': '打游戏', 'phase': ('2019/5/17', '1:30', '4:20'), 'tags': '娱乐'},
            {'title': '打篮球', 'phase': ('2019/5/17', '18:00', '19:15'), 'tags': '运动'}
        ]

        with open('./data/tasks','r') as f:
            tasks_to_show = filter_date([json.loads(x.strip('\n')) for x in f.readlines()], date_to_show)
        #draw new pie
        pie_data = {x['tags']:self.time_len([x['phase'][1], x['phase'][2]]) for x in tasks_to_show}
        print('pie data is {}'.format(pie_data))
        self.draw_pie(pie_data, date_to_show)
        self.draw_timeline(tasks_to_show)
        #draw new timeline

    def draw_pie(self, data, today):
        # if not data:
        #     return

        self.F = MyFigure(width=3, height=2)

        values = [x for x in data.values()]
        labels = [x for x in data.keys()]
        #colors = ['#7199cf', '#4fc4aa', '#ffff10']
        colors_sample = []
        for i in range(len(values)):
            colors_sample.append(self.colors[i % len(self.colors)])
        print(colors_sample)
        # 设置饼图的凸出显示
        explode = [0 for i in range(len(values))]
        self.F.axes.pie(values, labels=labels, colors=colors_sample, explode=explode, shadow=False)
        self.F.fig.suptitle(today)

        # graphicscene是一个展示2D图形的场景，setSceneRect的效果是设置场景中可见的矩形范围
        # 参数a b c d; a是可见范围左上角坐标的横坐标 b是纵坐标； c是可见范围的横向距离，d是纵向距离
        # graphicscene.setSceneRect(QtCore.QRectF(101, 300, 590, 100))
        graphicscene = QtWidgets.QGraphicsScene()
        graphicscene.addWidget(self.F)
        graphicscene.setSceneRect(QtCore.QRectF(101, 300, 590, 100))
        self.graphicview.setScene(graphicscene)

    def draw_timeline(self, data):

        def sort_func(elem):
            t = elem['phase'][1].split(':')
            t = [int(x) for x in t]
            return t[0]*60+t[1]

        for i in range(self.vlay_2.count()):
            self.vlay_2.itemAt(i).widget().deleteLater()

        if not data:
            temp = QLabel("还没有任务完成~", self)
            temp.setStyleSheet('background-color: red; margin: 0px; font-size:20px;color:black')
            temp.setFixedHeight(60)
            temp.setFixedWidth(345)
            self.vlay_2.addWidget(temp)
            self.vlay_2.addWidget(QLabel())
            return

        #数据项x格式  {'title': '程设', 'phase': ('2019/5/17', '8:00', '10:50'), 'tags': '学习'},
        data.sort(key=sort_func)
        index = -1;
        head_time = 0
        for x in data:
            index += 1
            temp = QLabel(x['title'],self)
            temp.setToolTip('标签:{}\n时间：{} ~ {}'.format(x['tags'], x['phase'][1], x['phase'][2]))
            begin_point ,end_point = self.time_transform(x['phase'][1],x['phase'][2])

            if head_time != begin_point:
                blank = QLabel('none',self)
                #blank.setStyleSheet('margin: 0px; font-size:20px;color:black')
                #blank.setStyleSheet('background-color: purple; margin: 0px; font-size:20px;color:black')
                blank.setFixedWidth(345)
                if begin_point <= head_time:
                    print('error!!!')
                blank.setFixedHeight(2*(begin_point-head_time))
                #blank.setFixedHeight(100)

                self.vlay_2.addWidget(blank)
                head_time = end_point
                print(index)

            temp.setStyleSheet("background-color: {}; margin: 0px; font-size:20px;color:black".format(self.colors[index % len(self.colors)]))
            #temp.setStyleSheet("background-color: rgb(144,237,15); margin: 0px; font-size:20px;color:black")
            temp.setFixedWidth(345)
            temp.setFixedHeight(2*(end_point-begin_point))
            self.vlay_2.addWidget(temp)
        self.vlay_2.addWidget(QLabel())

    def setScrollArea(self):
        self.scrollArea = QtWidgets.QScrollArea(self)
        self.upest.addWidget(self.scrollArea)
        self.scrollArea.resize(1000, 1000)
        self.scrollcontent = QWidget()
        self.setMinimumHeight(10)  ###important

        self.lay1 = QHBoxLayout(self)
        self.lay1.setContentsMargins(0,0,0,0)
        self.lay1.setSpacing(0)

        self.vlay_1 = QVBoxLayout(self)
        self.vlay_1.setContentsMargins(0, 0, 0, 0)
        self.vlay_1.setSpacing(0)

        self.vlay_2 = QVBoxLayout(self)
        self.vlay_2.setContentsMargins(0, 0, 0, 0)
        self.vlay_2.setSpacing(0)
        for i in range(24):
            temp = QLabel("{}:00~{}:00".format(str(i),str(i+1)))
            if i % 2 ==0:
                temp.setStyleSheet('background-color: purple; margin: 0px; font-size:20px;color:black')
                # temp.setStyleSheet('margin: 0px; border:2px solid red; border-left: 0px; font-size:20px;color:black')
            else:
                temp.setStyleSheet('background-color: rgb(232, 234, 212); margin: 0px; font-size:20px;color:black')
            temp.setFixedHeight(120)
            temp.setFixedWidth(200)
            self.vlay_1.addWidget(temp)

        self.draw_timeline(self.initial_timeline)

        self.lay1.addLayout(self.vlay_1)
        self.lay1.addLayout(self.vlay_2)
        self.scrollcontent.setLayout(self.lay1)
        self.scrollArea.setWidget(self.scrollcontent)

    def setPie(self):
        self.graphicview = QtWidgets.QGraphicsView()
        self.graphicview.horizontalScrollBar().setVisible(False)
        self.draw_pie(self.initial_pie, self.date_list[-1])
        self.graphicview.show()
        self.upest.addWidget(self.graphicview)

    def setIcon(self):
        self.setWindowIcon(QIcon('./images/others/icon.png'))

    def SetWindoww(self):
        self.move(403, 36)
        #self.resize(1200,900)
        self.setFixedSize(1200, 900)
        self.setWindowTitle('觅时')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = main()
    sys.exit(app.exec_())