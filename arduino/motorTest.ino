#include <Servo.h>
//60-150
//Serial port:
  //start: s
  //close: c
const int throttlePin = 9;
const int reverseBrakePin = 10;
const int secondPin = 11;

Servo motor1;
Servo motor2;

unsigned long lastChangeTime = 0;
int motorSpeed = 0;
bool motorRunning = false; 

int speedStages[] = {0, 60, 90, 120, 150, 180};
int percentages[] = {0, 20, 40, 60, 80, 100}; 
int currentStage = 0;

const unsigned long stageDuration = 2000;

void setup() {
  Serial.begin(9600);

  motor1.attach(throttlePin);
  motor2.attach(secondPin);
  motor1.write(0);
  motor2.write(0);
  delay(1000);

  lastChangeTime = millis();
}

void loop() {
  unsigned long currentTime = millis();

  if (Serial.available() > 0) {
    char command = Serial.read();
    
    if (command == 's' || command == 'S') {
      motorRunning = true;
      currentStage = 0; 
      lastChangeTime = millis(); 
      Serial.println("Motor started.");
    } 
    else if (command == 'c' || command == 'C') {
      motor1.write(0); 
      motor2.write(0); 
      motorRunning = false;
      Serial.println("Motor stopped.");
    }
  }

  if (motorRunning) {
    if (currentTime - lastChangeTime >= stageDuration) {
      motorSpeed = speedStages[currentStage];
      int percent = percentages[currentStage];

      motor1.write(motorSpeed);
      motor2.write(motorSpeed);
      Serial.print("Motor speed: ");
      Serial.print(motorSpeed);
      Serial.print(" | Percentage: ");
      Serial.print(percent);
      Serial.println("%");

      currentStage++;

      if (currentStage >= 6) { 
        motor1.write(0); 
        motor2.write(0); 
        motorRunning = false;  
        Serial.println("Motor stopped.");
      }

      lastChangeTime = currentTime;
    }
  }
}


// int xVal = analogRead(Xin);
  // int yVal = analogRead(Yin);
  
  // if (xVal < 520 && yVal == 520) {
  //   motorSpeed = map(xVal, 0, 520, 90, 0);
  // } else if (xVal > 520 && yVal == 520) {
  //   motorSpeed = map(xVal, 520, 1023, 0, 180);
  // } else if (xVal == 520 && yVal == 520) {
  //   motorSpeed = 0;
  // } else if (yVal < 520 && xVal == 520) {
  //   motorSpeed = map(yVal, 0, 520, 60, 0);
  // } else if (yVal > 520 && xVal == 520) {
  //   motorSpeed = map(yVal, 520, 1023, 0, 135);
  // }

  // if (Serial.available() > 0) {
  //   int percent = Serial.parseInt();
  //   if (percent >= 0 && percent <= 100) {
  //     motorSpeed = map(percent, 0, 100, 0, 180);
  //     if (percent > 0) {  
  //       Serial.print("Serial input percent: ");
  //       Serial.print(percent);
  //       Serial.print(" | Motor speed: ");
  //       Serial.println(motorSpeed);
  //     }
  //     lastUpdateTime = currentTime;
  //     updateMotor = true;
  //   } else {
  //     Serial.println("Invalid percent value. Enter a value between 0 and 100.");
  //   }
  // }

  // if (updateMotor && (currentTime - lastUpdateTime == 0)) {
  //   motor.write(motorSpeed);
  //   Serial.println(motorSpeed);
  //   Serial.println(currentTime);
  // } else if (currentTime - lastUpdateTime > 5000) {
  //   updateMotor = false;
  // }
