#include <Servo.h>

// Speed range: 60-150
// Serial port commands:
// Start: s
// Stop: c

const int throttlePin1 = 9;  // Motor 1 connected to pin 9
const int throttlePin2 = 10; // Motor 2 connected to pin 10

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

  motor1.attach(throttlePin1);
  motor2.attach(throttlePin2);
  
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
      Serial.println("Motors started.");
    } else if (command == 'c' || command == 'C') {
      motor1.write(0);
      motor2.write(0);
      motorRunning = false;
      Serial.println("Motors stopped.");
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
        Serial.println("Motors stopped.");
      }

      lastChangeTime = currentTime;
    }
  }
}
