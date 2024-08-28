#include <Servo.h>

Servo motor1;
Servo motor2;

void setup() {
    motor1.attach(9);  
    motor2.attach(10);
    Serial.begin(9600);
}

void loop() {
    if (Serial.available()) {
        char command = Serial.read();

        if (command == 's') {
            motor1.write(60);
            motor2.write(60); 
        } else if (command == 'c') {
            motor1.write(0);
            motor2.write(0);
        }
    }
}
