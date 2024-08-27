# MotorSpeedControl
This is a Python application built using PyQt5 and PyQtGraph to control a motor via an Arduino and display real-time speed data in a graph. The application also displays the current time and frequency.

## Features

- **Motor Control:** Start and stop the motor using GUI buttons.(Speed runs from 0% to 100%, with a 20% increase each 2 seconds respectively)
- **Real-Time Speed Graph:** Displays motor speed over time with smooth cubic interpolation for a better visual experience.
- **Status Updates:** Displays the current speed and percentage of the motor speed stages.
- **Time Display:** Shows the current time and date in a formatted label.
- **Frequency Indicator:** Randomly generated frequency values displayed in the GUI.

## Prerequisites

- Python 3.x
- Arduino connected via serial port (configured for COM13 at 9600 baud rate)
- Required Python packages:
  - PyQt5
  - PyQtGraph
  - SciPy
  - NumPy
  - PySerial

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/clairebear0508/ARRC_motor_control.git
   cd MotorControlApp

2. **Install Python packages:**
pip install pyqt5 pyqtgraph scipy numpy pyserial

3. **Run the Application:**
python motorTestSpeed.py
