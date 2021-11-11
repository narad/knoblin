#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// From the original driver demo:
// called this way, it uses the default address 0x40
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();
// you can also call it with a different address you want
//Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x41);

// Depending on your servo make, the pulse width min and max may vary, you 
// want these to be as small/large as possible without hitting the hard stop
// for max range. You'll have to tweak them as necessary to match the servos you
// have!
#define SERVOMIN  125 // this is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX  575 // this is the 'maximum' pulse length count (out of 4096)


String inByte;  // byte read from port, can come from Python script
String c_pos;   // read byte encoding of servo position
String c_servo; // read byte encoding target servo
String c_delay; // read byte encoding delay to servo speed
int pos;        // target servo position as an Int
int servo;      // target servo ID as an Int
int last;       // last position as an Int
int delay_time = 0; // delay between servo move increments


void setup() {
  Serial.begin(9600);
  Serial.println("Initializing.");
  pwm.begin();
  pwm.setPWMFreq(60);  // Analog servos run at ~60 Hz updates
  last = -1;
}


void loop() {    
  if(Serial.available()) { // if data available in serial port
    // read data until newline
    inByte = Serial.readStringUntil('\n'); 
    Serial.println(inByte);

    // Unpack servo and position ID from byte sent on comm port
    c_servo = inByte.substring(0, 1);
    c_pos = inByte.substring(2, inByte.length());

    // Convert to int
    servo = c_servo.toInt();
    pos = c_pos.toInt();  
//    delay_time = c_delay.toInt(); local delay time deprecated

    // Move the servo
    if (last == -1 || delay_time == 0) {
      pwm.setPWM(servo, 0, pos);
      last = pos;
    }
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
