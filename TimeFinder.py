# -*- coding: utf-8 -*-
# V3.1 修复时间轴绘制出错bug
from sys import argv, exit
import background_rc
import stop_rc
from os import path
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QIcon
from PyQt5.QtCore import QRect, Qt, QSize, QTime, QDateTime, QDate, QTimer
from PyQt5.QtWidgets import (QApplication,QWidget,QVBoxLayout,QHBoxLayout,QDesktopWidget, QAction, QFileDialog, QLCDNumber, QLabel, QToolButton,
                             QSlider, QInputDialog, QMessageBox)
from PyQt5.QtWidgets import QMainWindow, QPushButton
from statistic import statistic

from json import dumps
from analysis import analysis
from pygame import mixer


class timer(QMainWindow):
    def __init__(self):
        super(timer, self).__init__()
        self.initial_variables() #zd
        self.init_ui()
        self.show()

    def init_ui(self):
        self.time = QTimer(self)
        self.time.setInterval(1000)
        self.time.timeout.connect(self.refresh)
        self.time.timeout.connect(self.skip_day) #zd

        self.time_start_up=QTime(0, 0, 0)#正计时的开始时间
        self.time_start_fall=QTime(23,59,59)#倒计时结束时分秒
        self.time_start_data=QDate.currentDate()#倒计时结束年月日

        self.time_system=QTimer(self)
        self.time_system.setInterval(1000)
        self.time_system.timeout.connect(self.refresh_system)
        self.time_system.start()

        self.hour=0#暂停前已经记录的时分秒
        self.minute=0
        self.second=0
        self.interval=0

        self.time.start()

        self.init_window()
        self.init_lcd()
        self.init_Button()
        self.init_bar()
        self.init_label()

    def init_window(self):
        self.resize(900, 600)
        self.setWindowTitle('觅时')
        self.setWindowIcon(QIcon('./images/others/icon.png'))
        self.image_file="./images/background/timg.png"
        mixer.init()
        self.sound=mixer.music.load("./sound/Berliner Philharmoniker.mp3")#默认背景音乐
        mixer.music.play(-1, 0.0)

    def init_bar(self):
        self.statusBar()
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        background_menu = menubar.addMenu('背景图片')
        sound_menu = menubar.addMenu('背景音乐')
        model_menu=menubar.addMenu('窗口模式')

        self.open_picture_action = QAction('本地图片', self)
        background_menu.addAction(self.open_picture_action)
        self.open_picture_action.triggered.connect(self.open_picture)

        self.open_music_action = QAction('本地音乐', self)
        self.stop_music_action = QAction('音乐暂停', self)
        self.continue_music_action = QAction('音乐继续', self)
        self.start_music_action = QAction('从头播放', self)
        sound_menu.addAction(self.open_music_action)
        sound_menu.addAction(self.stop_music_action)
        sound_menu.addAction(self.continue_music_action)
        sound_menu.addAction(self.start_music_action)
        self.open_music_action.triggered.connect(self.open_music)
        self.stop_music_action.triggered.connect(self.stop_music)
        self.continue_music_action.triggered.connect(self.continue_music)
        self.start_music_action.triggered.connect(self.start_music)

        self.float_action=QAction('悬浮窗',self)
        self.normal_action=QAction('正常窗口',self)
        model_menu.addAction(self.float_action)
        model_menu.addAction(self.normal_action)
        self.float_action.triggered.connect(self.float)
        self.normal_action.triggered.connect(self.normal)

    def open_picture(self):
        #选择本地图片
        self.image_file, _ = QFileDialog.getOpenFileName(self, 'Open file', './images/background', 'Image files (*.jpg *.gif *.png *.jpeg)')
        self.setAutoFillBackground(True)
        if path.exists(self.image_file)==False:
            return
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(self.image_file).scaled(self.size(),Qt.IgnoreAspectRatio,Qt.SmoothTransformation)))
        self.setPalette(palette)

    def open_music(self):
        #选择本地音乐
        self.music_file, _ = QFileDialog.getOpenFileName(self, 'Open file', './sound',
                                                         'Image files (*.mp3 *.wan *.midi)')
        if path.exists(self.music_file)==False:
            return
        mixer.init()
        self.sound=mixer.music.load(self.music_file)
        mixer.music.play(-1, 0.0)

    def stop_music(self):
        #音乐暂停
        mixer.music.pause()

    def continue_music(self):
        #音乐继续
        mixer.music.unpause()

    def start_music(self):
        #音乐从头开始
        mixer.music.play()

    def init_lcd(self):
        #正计时LCD
        self.lcd1 = QLCDNumber(self)
        self.lcd1.setStyleSheet("background: transparent;font-size:50000px")
        self.lcd1.setObjectName("lcd1")
        self.lcd1.setDigitCount(12)
        self.lcd1.setMode(QLCDNumber.Dec)
        self.lcd1.setSegmentStyle(QLCDNumber.Flat)
        self.lcd1.setVisible(True)

        #倒计时LCD
        self.lcd2 = QLCDNumber(self)
        self.lcd2.setStyleSheet("background: transparent;font-size:50000px")
        self.lcd2.setObjectName("lcd2")
        self.lcd2.setDigitCount(12)
        self.lcd2.setMode(QLCDNumber.Dec)
        self.lcd2.setSegmentStyle(QLCDNumber.Flat)
        self.lcd2.setVisible(False)

        #系统时间LCD
        self.lcd3 = QLCDNumber(self)
        self.lcd3.setStyleSheet("background: transparent;font-size:50000px;color:rgb(255,255,255)")
        self.lcd3.setObjectName("lcd3")
        self.lcd3.setDigitCount(12)
        self.lcd3.setMode(QLCDNumber.Dec)
        self.lcd3.setSegmentStyle(QLCDNumber.Flat)

    def init_label(self):
        #显示标签
        self.label=QLabel("",self)
        self.label.setVisible(True)
        self.label.setFixedWidth(500)
        self.label.setFixedHeight(100)
        self.setStyleSheet("QLabel{font-size:30px;font-weight:normal;font-family:Arial;}")
        self.label.setGeometry(QRect(300, 100, 20, 11))

    def float(self):
        #进入悬浮窗
        self.hide()
        self.resize(550, 60)
        # self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
        self.lcd3.setVisible(False)
        self.splider.setVisible(False)
        self.label.setVisible(False)
        #self.setWindowFlags(Qt.WindowMaximizeButtonHint)
        self.setWindowFlags(Qt.FramelessWindowHint|Qt.WindowStaysOnTopHint)


        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(
            QPixmap(self.image_file).scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
        self.setPalette(palette)

        self.show()
        self.showNormal()

    def normal(self):
        #退出悬浮窗
        self.hide()
        self.resize(900, 500)
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 3)
        self.setWindowFlags(Qt.Widget)
        self.lcd3.setVisible(True)
        self.splider.setVisible(True)
        self.label.setVisible(True)
        self.show()

    def resizeEvent(self, *args, **kwargs):
        width=self.width()
        height=self.height()
        self.lcd1.setGeometry(QRect((width-300)/2, (height-111)/2, 300, 111))
        self.lcd2.setGeometry(QRect((width - 300) / 2, (height - 111) / 2, 300, 111))
        self.lcd3.setGeometry(QRect(width - 200, height - 100, 200, 111))
        self.label.setGeometry(QRect((width - 75) / 2, height / 2, 300, 111))

        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap(self.image_file).scaled(self.size(),Qt.IgnoreAspectRatio,Qt.SmoothTransformation)))
        self.setPalette(palette)

    def init_Button(self):
        #开始结束按钮
        self.state_start_end=0
        self.pushButton = QPushButton()
        self.pushButton.setStyleSheet("background:transparent;")
        self.pushButton.setText("")
        icon = QIcon()
        icon.addPixmap(QPixmap(":/start/start.png"))
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QSize(30, 30))
        self.pushButton.setCheckable(True)
        self.pushButton.setFlat(True)
        self.pushButton.setObjectName("开始/结束")
        self.pushButton.clicked.connect(self.start_end)

        #暂停继续按钮
        self.state_continue_stop = 0
        self.pushButton_2 = QPushButton()
        self.pushButton_2.setStyleSheet("background:transparent;")
        self.pushButton_2.setText("")
        icon1 = QIcon()
        icon1.addPixmap(QPixmap(":/on/stop.png"))
        self.pushButton_2.setIcon(icon1)
        self.pushButton_2.setIconSize(QSize(30, 30))
        self.pushButton_2.setCheckable(True)
        self.pushButton_2.setFlat(True)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.continue_stop)

        #数据分析按钮
        self.toolButton = QToolButton()
        self.toolButton.setLayoutDirection(Qt.LeftToRight)
        self.toolButton.setStyleSheet("background:transparent;")
        icon2 = QIcon()
        icon2.addPixmap(QPixmap(":/analytics/analytics.png"), QIcon.Normal, QIcon.Off)
        self.toolButton.setIcon(icon2)
        self.toolButton.setIconSize(QSize(30, 30))
        self.toolButton.setAutoRaise(True)
        self.toolButton.setObjectName("toolButton")
        self.toolButton.clicked.connect(self.analyze)

        #声音播放静音按钮
        self.sound_state=0
        self.pushButton_4 = QPushButton()
        self.pushButton_4.setStyleSheet("background:transparent;")
        self.pushButton_4.setText("")
        icon3 = QIcon()
        icon3.addPixmap(QPixmap(":/sound/sound.png"), QIcon.Normal, QIcon.Off)
        icon3.addPixmap(QPixmap(":/sound_off/Sound_off.png"), QIcon.Normal, QIcon.On)
        self.pushButton_4.setIcon(icon3)
        self.pushButton_4.setIconSize(QSize(30, 30))
        self.pushButton_4.setCheckable(True)
        self.pushButton_4.setFlat(True)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.sound_renew)
        #self.pushButton_4.rclicked.connect(self.sound_renew())

        #声音大小调节按钮
        self.splider = QSlider(Qt.Horizontal)
        self.splider.valueChanged.connect(self.valChange)
        self.splider.setMinimum(0)
        self.splider.setMaximum(100)
        self.splider.setSingleStep(1)
        self.splider.setTickInterval(1)
        self.splider.setValue(100)

        #布局
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        hbox.addWidget(self.pushButton)
        hbox.addWidget(self.pushButton_2)
        hbox.addWidget(self.toolButton)
        hbox.addWidget(self.pushButton_4)
        hbox.addWidget(self.splider)
        hbox.addStretch(1)
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        main_frame = QWidget()
        main_frame.setLayout(vbox)
        self.setCentralWidget(main_frame)

    def refresh(self):
        #正计时
        self.startDate_up = QDateTime(QDate.currentDate(), self.time_start_up).toMSecsSinceEpoch()#显示正计时
        self.endDate_up = QDateTime.currentMSecsSinceEpoch()
        interval_up = self.endDate_up - self.startDate_up+self.interval
        if interval_up > 0:
            hour = interval_up // (60 * 60 * 1000)
            min = (interval_up - hour * 60 * 60 * 1000) // (60 * 1000)
            sec = (interval_up - hour * 60 * 60 * 1000 - min * 60 * 1000) // 1000
            intervals =  '0' * (2 - len(str(hour))) + str(hour) + ':' + '0' * (2 - len(str(min))) +str(min) + ':' + '0' * (2 - len(str(sec))) +str(sec)
            self.lcd1.display(intervals)


        #倒计时
        self.startDate_fall = QDateTime.currentMSecsSinceEpoch()#显示倒计时
        self.endDate_fall = QDateTime(self.time_start_data, self.time_start_fall).toMSecsSinceEpoch()
        interval_fall = self.endDate_fall - self.startDate_fall-self.interval
        if interval_fall > 0:
            hour = interval_fall // (60 * 60 * 1000)
            min = (interval_fall - hour * 60 * 60 * 1000) // (60 * 1000)
            sec = (interval_fall - hour * 60 * 60 * 1000 - min * 60 * 1000) // 1000
            intervals = '0' * (2 - len(str(hour))) + str(hour) + ':' + '0' * (2 - len(str(min))) + str(
                min) + ':' + '0' * (2 - len(str(sec))) + str(sec)
            self.lcd2.display(intervals)
            if hour==0 and min==0 and sec==0:
                mixer.init()
                self.sound = mixer.music.load("./sound/My Soul,Your Beats!.mp3")
                mixer.music.play(-1, 0.0)

    def refresh_system(self):
        hour=QTime.currentTime().hour()#显示系统时间
        min=QTime.currentTime().minute()
        sec = QTime.currentTime().second()
        intervals = '0' * (2 - len(str(hour))) + str(hour) + ':' + '0' * (2 - len(str(min))) + str(
            min) + ':' + '0' * (2 - len(str(sec))) + str(sec)
        self.lcd3.display(intervals)

    def sound_renew(self):
        #背景音乐状态按钮
        #if self.pushButton_4 == Qt.LeftButton:
        if self.sound_state==0:
            self.sound_state=1
            mixer.music.set_volume(0.0)
            self.splider.setValue(0)
            self.splider.setEnabled(False)

        else:
            self.sound_state=0
            mixer.music.set_volume(1.0)
            self.splider.setValue(100)
            self.splider.setEnabled(True)

    def valChange(self):
        #设置音量为滑动条音量
        mixer.music.set_volume(self.splider.value()/100)

    def start_end(self):
        time_1 = QTimer(self)
        time_1.setInterval(1)
        time_1.timeout.connect(self.state_refresh)
        time_1.start()

        if self.state_start_end%2==0:
            #任务开始
            self.state_continue_stop=1
            self.statis = statistic()
            self.interval=0
            self.time.start()


        if self.state_start_end%2==1:
            #任务结束
            self.check="无"
            text, ok = QInputDialog.getText(self, '任务备注', '任务备注')
            if ok:
                now_end = QDate.currentDate()
                print(now_end.toString(Qt.DefaultLocaleLongDate))#结束时的年月日
                time_end = QTime.currentTime()
                print(time_end.toString(Qt.DefaultLocaleLongDate))#结束时的时分秒
                self.new_check = QLabel(text)
                self.check=self.new_check.text()
                print('任务备注=%s' % self.check)#title

                self.set_end(time_end.toString(Qt.DefaultLocaleLongDate), self.check)#zd

                icon = QIcon()
                icon.addPixmap(QPixmap(":/start/start.png"))
                self.pushButton.setIcon(icon)
                icon1 = QIcon()
                icon1.addPixmap(QPixmap(":/on/stop.png"))
                self.pushButton_2.setIcon(icon1)

                if self.statis.time_button==1:
                    mixer.music.stop()
                    mixer.music.load("./sound/Berliner Philharmoniker.mp3")
                    mixer.music.play(-1, 0.0)

                self.time.stop()
            else:
                #没有确认退出
                self.state_start_end+=1
        self.state_start_end += 1

    def state_refresh(self):
        if self.statis.state==1:
            self.statis.state=0
            #print(self.statis.label_return)#标签
            start = QDate.currentDate()
            #print(start.toString(Qt.DefaultLocaleLongDate))#开始的年月日
            time_start = QTime.currentTime()
            print(time_start.toString(Qt.DefaultLocaleLongDate))#开始的时分秒
            self.set_begin(start.toString(Qt.DefaultLocaleLongDate),  #zd
                           time_start.toString(Qt.DefaultLocaleLongDate),
                           self.statis.label_return)
            icon = QIcon()
            icon.addPixmap(QPixmap(":/over/over.png"))
            self.pushButton.setIcon(icon)
            icon1 = QIcon()
            icon1.addPixmap(QPixmap(":/stop/on.png"))
            self.pushButton_2.setIcon(icon1)
            self.label.setText(self.statis.label_return)

            if self.statis.time_button==0:
                self.time_start_up=time_start
                self.lcd1.setVisible(True)
                self.lcd2.setVisible(False)
            else:
                hour=int(time_start.hour())+int(self.statis.hour_time_return)
                minute = int(time_start.minute()) + int(self.statis.minute_time_return)
                second = int(time_start.second()) + int(self.statis.second_time_return)
                if hour>=24:
                    hour-=24
                    self.time_start_data=start.addDays(1)
                self.time_start_up = time_start
                self.time_start_fall = QTime(hour, minute, second)
                self.lcd1.setVisible(False)
                self.lcd2.setVisible(True)

        if self.statis.state==2:
            self.statis.state=0
            self.state_start_end += 1

    def continue_stop(self):
        #暂停继续
        self.state_continue_stop += 1
        if self.state_start_end%2==1 and self.state_continue_stop % 2 ==1:
            self.statis.state = 1
            self.state_refresh()
            icon1 = QIcon()
            icon1.addPixmap(QPixmap(":/stop/on.png"))
            self.pushButton_2.setIcon(icon1)
            self.time.start()

        if self.state_start_end%2==1 and self.state_continue_stop%2==0:
            self.check="无"
            text, ok = QInputDialog.getText(self, '任务备注', '任务备注')
            if ok:
                now_end = QDate.currentDate()
                print(now_end.toString(Qt.DefaultLocaleLongDate))#结束时的年月日
                time_end = QTime.currentTime()
                print(time_end.toString(Qt.DefaultLocaleLongDate))#结束时的时分秒
                self.new_check = QLabel(text)
                self.check=self.new_check.text()
                print('任务备注=%s' % self.check)#title
                self.set_end(time_end.toString(Qt.DefaultLocaleLongDate), self.check) #zd
                self.set_begin(now_end.toString(Qt.DefaultLocaleLongDate),
                               time_end.toString(Qt.DefaultLocaleLongDate),
                               '')
                icon1 = QIcon()
                icon1.addPixmap(QPixmap(":/on/stop.png"))
                self.pushButton_2.setIcon(icon1)

                self.interval+=self.time_start_up.msecsTo(time_end)
                if self.interval<0:
                    self.interval+=86400 * 1000

                self.time.stop()
            else:
                self.state_continue_stop+=1



    #每次开始会调用
    def set_begin(self, year, begin_time, tags): # zd
        # 年的格式转化
        self.task_is_on = True
        def year_transform(year):
            new_year = ''
            for i in year:
                if i >= '0' and i <= '9':
                    new_year = new_year + i
                else:
                    new_year = new_year + '/'
            return new_year[:-1]

        self.year = year_transform(year)
        self.begin_time = begin_time
        if tags:
            self.tags = tags

    #结束或者暂停会调用 用于写入数据库
    def set_end(self, end_time, title): #zd
        self.task_is_on = False
        # 判断是否大于1分钟，是则返回true否则false
        def cmp_1min(time1, time2):
            # print('begin compare')
            #print(time1+' '+time2)
            t1 = time1.split(':')
            t1 = [int(x) for x in t1]
            t2 = time2.split(':')
            t2 = [int(x) for x in t2]
            # print('interval is {}'.format(60*( 60*(t2[0]-t1[0])+(t2[1]-t1[1]) )+(t2[2]-t1[2])))
            return 60*( 60*(t2[0]-t1[0])+(t2[1]-t1[1]) )+(t2[2]-t1[2]) >= 60


        if not cmp_1min(self.begin_time, end_time):
            print('小于1分钟，不予计入')
            QMessageBox.warning(self, '提示', '小于1分钟，不予计入',QMessageBox.Yes)
            return
        obj = {
            'title':title,
            'phase':(self.year, self.begin_time, end_time),
            'tags':self.tags
        }
        if not obj['title']:
            obj['title'] = '(无)'

        print(obj)
        with open('./data/tasks','a') as f:
            f.write(dumps(obj)+'\n')

        with open('./data/date_list','r') as f:
            date_list = [x.strip() for x in f.readlines()]
            if self.year in date_list:
                return
        with open('./data/date_list','a') as f:
            f.write(self.year+'\n')
        print('加入新日期')

    #调用数据分析窗口
    def analyze(self):
        self.anayze_window_opened = True
        self.anayze_window = analysis()

    def closeEvent(self, QCloseEvent):
        res = QMessageBox.question(self, '消息', '是否关闭这个窗口？', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if res==QMessageBox.Yes:
            if self.anayze_window_opened:
                self.anayze_window.close()
            if self.task_is_on:
                self.set_end(QTime.currentTime().toString(Qt.DefaultLocaleLongDate),'(无任务名)')
            QCloseEvent.accept()

        else:
            QCloseEvent.ignore()

    def initial_variables(self): #zd
        self.anayze_window_opened = False
        self.task_is_on = False
        self.year = ''
        self.tt = 0

    def skip_day(self):
        if not self.task_is_on:
            return
        # 年的格式转化
        def year_transform(year):
            new_year = ''
            for i in year:
                if i >= '0' and i <= '9':
                    new_year = new_year + i
                else:
                    new_year = new_year + '/'
            return new_year[:-1]
        #last_time = QTime.currentTime().toString(Qt.DefaultLocaleLongDate)
        last_date = QDate.currentDate().toString(Qt.DefaultLocaleLongDate)
        if self.year!=year_transform(last_date):
            print('天数不同！！！')
            self.set_end('23:59:59', '(无)')
            self.set_begin(last_date, '00:00:00', self.tags)

    def test(self):
        self.tt += 1
        print('悬浮窗第{}次'.format(self.tt))

if __name__ == "__main__":
    app = QApplication(argv)
    w = timer()
    exit(app.exec_())