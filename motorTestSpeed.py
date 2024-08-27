import serial
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
import pyqtgraph as pg
import random  

class MotorControlApp(QWidget):
    def __init__(self):
        super().__init__()

        self.current_frequency = 0  
        self.initUI()
        self.serial_port = serial.Serial('COM13', 9600, timeout=1)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_for_response)
        self.timer.start(1000)

        self.time_timer = QTimer(self)
        self.time_timer.timeout.connect(self.update_time)
        self.time_timer.start(1000)  

        self.update_time()  

    def initUI(self):
        self.setWindowIcon(QIcon('pics/ARRClogo.png')) 

        self.logo_label = QLabel(self)
        self.logo_pixmap = QPixmap('pics/ARRClogo.png') 
        self.logo_label.setPixmap(self.logo_pixmap)
        self.logo_label.setScaledContents(True)
        self.logo_label.setFixedSize(200, 100) 

        self.time_label = QLabel(self)
        self.time_label.setText('Time: 00:00:00')

        header_layout = QHBoxLayout()
        header_layout.addWidget(self.logo_label)
        header_layout.addWidget(self.time_label)
        header_layout.addStretch()

        self.start_button = QPushButton('Start Motor', self)
        self.stop_button = QPushButton('Stop Motor', self)
        self.status_label = QLabel('Status: Disconnected', self)
        self.frequency_label = QLabel(f'Frequency: {self.current_frequency} Hz', self)

        self.start_button.clicked.connect(self.start_motor)
        self.stop_button.clicked.connect(self.stop_motor)
        
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.status_label)
        button_layout.addWidget(self.frequency_label)  

        # Graph
        self.graph_widget = pg.PlotWidget()
        self.graph_widget.setBackground('w')
        self.graph_widget.setTitle("Motor Speed Over Time")
        self.graph_widget.setLabel('left', 'Speed', 'RPM')
        self.graph_widget.setLabel('bottom', 'Time', 's')
        self.graph_widget.showGrid(x=True, y=True)
        self.graph_data = []  

        main_layout = QHBoxLayout()
        main_layout.addWidget(self.graph_widget)
        main_layout.addLayout(button_layout)  
        
        overall_layout = QVBoxLayout()
        overall_layout.addLayout(header_layout) 
        overall_layout.addLayout(main_layout)
        
        self.setLayout(overall_layout)
        self.setWindowTitle('Motor Control')

        self.apply_styles()

        self.show()

    def apply_styles(self):
        self.setStyleSheet("background-color: #444444;")  
        
        self.start_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50; 
                color: white;
                border: none;
                width: 100px; 
                height: 100px; 
                border-radius: 50px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 20px;
                cursor: pointer;
                border-radius: 50px;
                margin: 10 15px;                         
                font-family: Arial, Helvetica, sans-serif;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049; 
            }
        """)
        
        self.stop_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336; 
                color: white;
                border: none;
                width: 100px; 
                height: 100px;
                border-radius: 50px; 
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 20px;
                cursor: pointer;
                margin: 10 15px;
                border-radius: 50px;
                font-family: Arial, Helvetica, sans-serif;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #da190b; 
            }
        """)

        # Frequency label
        self.frequency_label.setStyleSheet("""
            QLabel {
                color: black;
                font-size: 20px;
                padding: 10px;
                text-align: center;
                background-color: #bdbdbd;
                border-radius: 10px;
                text-align: center;
                font-family: Arial, Helvetica, sans-serif;
            }
        """)

        # Status label
        self.status_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 20px;
                padding: 10px;
                background-color: #666666;
                border-radius: 10px;
                text-align: center;
                font-family: Arial, Helvetica, sans-serif;
            }
        """)

        # Time label
        self.time_label.setStyleSheet("""
            QLabel {
                font-size: 60px;
                font-weight: bold;
                color: #e0e0e0;
                padding: 10px;
                font-family: Arial, Helvetica, sans-serif;
            }
        """)


    def start_motor(self):
        if self.serial_port.is_open:
            self.serial_port.write(b's')
            self.status_label.setText('Status: Motor Starting...')
        else:
            self.status_label.setText('Status: Port Error')

    def stop_motor(self):
        if self.serial_port.is_open:
            self.serial_port.write(b'c')
            self.status_label.setText('Status: Motor Stopping...')
        else:
            self.status_label.setText('Status: Port Error')

    def check_for_response(self):
        if self.serial_port.in_waiting:
            response = self.serial_port.readline().decode().strip()
            self.status_label.setText(f'Status: {response}')
            self.update_graph(random.randint(0, 180))  

            self.current_frequency = random.randint(1, 100) 
            self.frequency_label.setText(f'Frequency: {self.current_frequency} Hz')

    def update_graph(self, speed):
        if len(self.graph_data) > 100: 
            self.graph_data.pop(0)
        self.graph_data.append(speed)
        self.graph_widget.clear()
        self.graph_widget.plot(self.graph_data, pen=pg.mkPen(color=(255, 0, 0), width=3))

    def update_time(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()

        time_str = current_time.toString('hh:mm:ss')
        am_pm = 'AM' if current_time.hour() < 12 else 'PM'\

        date_str = current_date.toString('yyyy/M/d')

        self.time_label.setText(f"{am_pm} {time_str} {date_str}")

    def closeEvent(self, event):
        self.serial_port.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MotorControlApp()
    sys.exit(app.exec_())