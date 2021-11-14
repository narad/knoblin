#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// This script is design for controlling any servo hooked up
// to a PCA9685 servo control unit via Arduino.  It controls
// one servo at a time.  To use it, use the Python serial.Serial
// package to send a byte message of the form "servo_id:position", 
// i.e. the String "1:350" moves the first servo to 350 (center, usually)


Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
String inByte;  // byte read from port, can come from Python script
String c_pos;   // read byte encoding of servo position
String c_servo; // read byte encoding target servo
String c_delay; // read byte encoding delay to servo speed
int pos;        // target servo position as an Int
int servo;      // target servo ID as an Int
int last;       // last position as an Int
int delay_time = 0; // delay between servo move increments


void setup() {
  // drastically reduce Serial.readStringUntil time
  Serial.setTimeout(250); 
  // initiate serial protocol
  Serial.begin(9600);
  Serial.println("Initializing.");
  // initiate servos
  pwm.begin();
  // Analog servos run at ~60 Hz updates
  pwm.setPWMFreq(60); 
  // set an initial 'last position'.  Once the servo is moved
  // and this updates, the servo can be moved incrementally
  last = -1;
}


void loop() {    
  if(Serial.available()) {
    message = Serial.readStringUntil('\n'); 
    Serial.println(message);

    // Unpack servo and position ID from byte sent on comm port
    c_servo = message.substring(0, 1);
    c_pos = message.substring(2, message.length());

    // Convert to int
    servo = c_servo.toInt();
    pos = c_pos.toInt();  

    // Move the servo
    // Moving without delay
    if (last == -1 || delay_time == 0) {
      pwm.setPWM(servo, 0, pos);
      last = pos;
    }
    // Moving incrementally with delay
    else if (last < pos) {
      while (last < pos) {
        pwm.setPWM(servo, 0, last);
        last += 1;
        delay(delay_time);
      }  
    }
    else {
      while (last > pos) {
        pwm.setPWM(servo, 0, last);
        last -= 1;
        delay(delay_time);
      }        
    }
  }
}
