import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPalette, QColor, QIcon


BASE_DIR = os.path.dirname(__file__)
MY_GREEN = '#11FF55'


class CountdownApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Task Timer')
        self.setGeometry(100, 100, 350, 100)

        # 第一行：输入框和按钮
        self.hour_input = QLineEdit('0')
        self.minute_input = QLineEdit('0')
        self.second_input = QLineEdit('0')
        self.start_button = QPushButton('Start')
        self.pause_button = QPushButton('Pause')
        self.hour_input.setFixedWidth(39)
        self.minute_input.setFixedWidth(39)
        self.second_input.setFixedWidth(39)
        self.start_button.setFixedWidth(95)
        self.pause_button.setFixedWidth(95)

        self.start_button.clicked.connect(self.start_countdown)
        self.pause_button.clicked.connect(self.pause_countdown)

        hbox1 = QHBoxLayout()
        # hbox1.addWidget(QLabel('Hours:'))
        hbox1.addWidget(self.hour_input)
        # hbox1.addWidget(QLabel('Minutes:'))
        hbox1.addWidget(self.minute_input)
        # hbox1.addWidget(QLabel('Seconds:'))
        hbox1.addWidget(self.second_input)
        hbox1.addWidget(self.start_button)
        hbox1.addWidget(self.pause_button)

        # 第二行：快速开始按钮
        self.quick_buttons = [
            QPushButton('30m'), QPushButton('20m'), QPushButton('10m'),
            QPushButton('5m'), QPushButton('3m'), QPushButton('2m')
        ]

        for button in self.quick_buttons:
            button.clicked.connect(self.quick_start)
            button.setFixedWidth(50)

        hbox2 = QHBoxLayout()
        for button in self.quick_buttons:
            hbox2.addWidget(button)

        # 第三行：备注和剩余时间显示
        self.note_input = QLineEdit()
        self.note_input.setFixedWidth(200)
        self.note_input.setStyleSheet("QLineEdit { font-size: 28px; }")
        self.time_display = QLineEdit('00:00:00')
        self.time_display.setReadOnly(True)
        self.time_display.setAlignment(Qt.AlignCenter)
        self.time_display.setStyleSheet(f"QLineEdit {{ font-size: 28px; background-color: {MY_GREEN}; }}")
        self.note_input.setFixedHeight(40)
        self.time_display.setFixedHeight(40)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.note_input)
        hbox3.addWidget(self.time_display)

        # 主布局
        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)

        self.setLayout(vbox)

        # 定时器
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.remaining_time = 0
        self.is_paused = False
        self.is_overtime = False
        self.overtime_timer = QTimer()
        self.overtime_timer.timeout.connect(self.flash_display)

    def start_countdown(self):
        hours = int(self.hour_input.text())
        minutes = int(self.minute_input.text())
        seconds = int(self.second_input.text())
        self.remaining_time = hours * 3600 + minutes * 60 + seconds
        self.is_paused = False
        self.timer.start(1000)
        self.overtime_timer.stop()
        self.is_overtime = False
        self.time_display.setStyleSheet(f"QLineEdit {{ font-size: 28px; background-color: {MY_GREEN}; }}")

    def pause_countdown(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.timer.stop()
        else:
            self.timer.start(1000)

    def quick_start(self):
        sender = self.sender()
        if sender == self.quick_buttons[0]:
            self.remaining_time = 30 * 60
        elif sender == self.quick_buttons[1]:
            self.remaining_time = 20 * 60
        elif sender == self.quick_buttons[2]:
            self.remaining_time = 10 * 60
        elif sender == self.quick_buttons[3]:
            self.remaining_time = 5 * 60
        elif sender == self.quick_buttons[4]:
            self.remaining_time = 3 * 60
        elif sender == self.quick_buttons[5]:
            self.remaining_time = 2 * 60

        self.is_paused = False
        self.timer.start(1000)
        self.overtime_timer.stop()
        self.is_overtime = False
        self.time_display.setStyleSheet(f"QLineEdit {{ font-size: 28px; background-color: {MY_GREEN}; }}")

    def update_time(self):
        self.remaining_time -= 1

        if self.remaining_time <= 0 and not self.is_overtime:
            self.is_overtime = True
            self.overtime_timer.start(500)

        sec_num = abs(self.remaining_time)
        hours = sec_num // 3600
        minutes = (sec_num % 3600) // 60
        seconds = sec_num % 60
        self.time_display.setText(f'{hours:02}:{minutes:02}:{seconds:02}')

    def flash_display(self):
        if self.time_display.palette().color(QPalette.Base) == QColor(MY_GREEN):
            self.time_display.setStyleSheet("QLineEdit { font-size: 28px; background-color: red; }")
        else:
            self.time_display.setStyleSheet(f"QLineEdit {{ font-size: 28px; background-color: {MY_GREEN}; }}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(BASE_DIR, 'tasktimer.ico')))
    ex = CountdownApp()
    ex.show()
    sys.exit(app.exec_())