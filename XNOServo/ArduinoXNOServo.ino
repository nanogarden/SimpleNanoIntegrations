#include <Servo.h>

Servo myservo;  // create servo object to control a servo

void setup() {
  Serial.begin(115200);
  myservo.attach(3);  // attaches the servo on pin 3 to the servo object
  myservo.write(90);  // Initialize servo position at the start
}

void loop() {
  if (Serial.available() > 0) {
    String message = Serial.readString();
    if (message == "trigger") {
       myservo.write(0);
      delay(800);
      myservo.write(180);
      delay(800);
      myservo.write(90);
    }
  }
}
