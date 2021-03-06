import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimediaWidgets import *
from PyQt5.QtMultimedia import *

# 녹화 확인 스택위젯
class ChkRecordingClicked(QLabel):
    def __init__(self, forBack, setting):
        super().__init__()
        self.list = QListWidget(self)
        self.setting = setting
        self.formSetting(forBack)

    def recordTest(self, item):
        self.recordPlay = PlayRecording(item.text(), self.setting)
        self.recordPlay.exec_()

    def fileList(self):
        self.list.clear()
        fileNames = os.listdir("Movie/")

        for fileName in fileNames:
            self.list.addItem('%s' % fileName)
        self.list.itemClicked.connect(self.recordTest)
        if(self.setting.thema=='D'):
            if (self.setting.fontSize2=='S'):
                self.list.setStyleSheet("color:white;font-size:18px;border:0px;QListWidget::item{border:1px solid red;};")
            elif (self.setting.fontSize2=='M'):
                self.list.setStyleSheet("color:white;font-size:20px;border:0px;QListWidget::item{border:1px solid red;};")
            else :
                self.list.setStyleSheet("color:white;font-size:22px;border:0px;QListWidget::item{border:1px solid red;};")
        else:
            if (self.setting.fontSize2=='S'):
                self.list.setStyleSheet("color:rgb(41,41,41);font-size:18px;border:0px;QListWidget::item{border:1px solid red;};")
            elif (self.setting.fontSize2=='M'):
                self.list.setStyleSheet("color:rgb(41,41,41);font-size:20px;border:0px;QListWidget::item{border:1px solid red;};")
            else :
                self.list.setStyleSheet("color:rgb(41,41,41);font-size:22px;border:0px;QListWidget::item{border:1px solid red;};")

        self.list.setFixedWidth(750)
        self.list.setFixedHeight(330)

    def formSetting(self, forBack):
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)
        if (self.setting.thema == 'D'):
            self.setStyleSheet("background-color:rgb(41,41,41)")
        else :
            self.setStyleSheet("background-color:white")

        self.quitLabel = QLabel()
        self.quitLabel.setFixedHeight(60)
        self.quitLabel.setFixedWidth(760)

        self.quitBtn = QPushButton("Quit")
        self.quitBtn.setFixedHeight(30)
        self.quitBtn.setFixedWidth(70)
        self.quitBtn.setStyleSheet("font:bold "+self.setting.fontSize+"px Arial; color:rgb(41,41,41); border:0px; border-radius:5px; background-color:rgb(106,230,197); outline:0px;")
        self.quitBtn.clicked.connect(forBack.changeStack)

        self.quitLayout = QGridLayout()
        self.quitLayout.setContentsMargins(0,0,0,0)
        self.quitLayout.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.quitLayout.addWidget(self.quitBtn)

        self.quitLabel.setLayout(self.quitLayout)

        self.layout.addWidget(self.list)
        self.layout.addWidget(self.quitLabel)


class PlayRecording(QDialog):
    def __init__(self, fileName, setting):
        super().__init__()
        self.setting = setting
        self.formSetting(fileName)

    def formSetting(self, fileName):
        if (self.setting.thema == 'D'):
            self.setStyleSheet("background-color:rgb(41,41,41)")
        else :
            self.setStyleSheet("background-color:white;")

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        container = QWidget()
        container.setFixedWidth(780)
        container.setFixedHeight(395)

        lay = QVBoxLayout(container)
        lay.setContentsMargins(10,10,10,15)
        lay.addWidget(videoWidget)

        backButton = QPushButton("Quit")
        backButton.setFixedWidth(70)
        backButton.setFixedHeight(30)
        backButton.setStyleSheet("font:bold "+self.setting.fontSize+"px Arial; color:rgb(41,41,41); border:0px; border-radius:5px; background-color:rgb(106,230,197); outline:0px;")
        backButton.clicked.connect(self.quit)

        self.playButton = QPushButton()
        self.playButton.setFixedWidth(30)
        self.playButton.setFixedHeight(30)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.setStyleSheet("background-color:white; border:0px; border-radius:5px; outline:0px;")
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.setFixedWidth(650)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 10)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(self.positionSlider)
        controlLayout.addWidget(backButton)

        layout = QVBoxLayout()
        layout.addWidget(container)
        layout.addLayout(controlLayout)

        self.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)

        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile('/home/pi/EL_IOT/raspberry pi/front/Movie/' + fileName)))
        self.mediaPlayer.play()

        self.showFullScreen()


    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def quit(self):
        self.close()
