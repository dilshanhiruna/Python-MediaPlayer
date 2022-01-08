from PyQt5.QtWidgets import QWidget, QPushButton, QStyle,QApplication,QPushButton, QHBoxLayout, QVBoxLayout, QSlider,QLabel,QFileDialog,QMessageBox
from PyQt5.QtGui import QPalette
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt,QUrl
import sys

class Window(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("PyPlayer")     
        self.setGeometry(350,100,700,500)

        p= self.palette()
        p.setColor(QPalette.Window, Qt.black)
        self.setPalette(p)

        self.createPlayer()

    def createPlayer(self):
        self.player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()
        self.openBtn = QPushButton("Open")
        self.openBtn.clicked.connect(self.open_file)

        self.playBtn = QPushButton("Play")
        self.playBtn.setEnabled(False)
        self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playBtn.clicked.connect(self.play_video)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0,0)
        self.labelDuration = QLabel()
        self.slider.sliderMoved.connect(self.set_position)

        

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0,0,0,0)
        hbox.addWidget(self.openBtn)
        hbox.addWidget(self.playBtn)
        hbox.addWidget(self.slider)
        hbox.addWidget(self.labelDuration)

        vbox = QVBoxLayout()
        vbox.addWidget(videoWidget)
        vbox.addLayout(hbox)

        self.player.setVideoOutput(videoWidget)

        self.setLayout(vbox)

        self.player.stateChanged.connect(self.media_state_changed)
        self.player.positionChanged.connect(self.position_changed)
        self.player.durationChanged.connect(self.duration_changed)
        self.slider.sliderMoved.connect(self.set_position)


    def open_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Video Files (*.mp4 *.avi *.mkv)")
        if filename != "":
            self.playBtn.setEnabled(True)
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))

    
    def play_video(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def media_state_changed(self,state):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playBtn.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
    def position_changed(self,position):
        self.slider.setValue(position)

    def duration_changed(self,duration):
        self.slider.setRange(0,duration)

    def set_position(self,position):
        self.player.setPosition(position)




app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())
