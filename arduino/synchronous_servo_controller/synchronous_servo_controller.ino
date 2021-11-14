#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// This script is design for controlling any servo hooked up
// to a PCA9685 servo control unit via Arduino.  It controls
// multiple servos "synchronously" -- updates are divided 
// into small intervals and sent to all servos iteratively 
// until the desired positons are reach.
// To use it, use the Python serial.Serial package to send a byte message 
// of the form "<3 digit servo-1 positon><3 digit servo-2 positon>...".
// Any position below the assigned min value (or above max) is ignored.
// For example: 
// The String "125000575" moves the first servo to 125 (likely the minimum)
// position, and the third servo to 575 (usually the maximum) psotion.


// Driver for servo controller
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

String message; // control message to receive over Serial protocol
int pos;        // target servo position as an Int
int servo;      // target servo ID as an Int
int delay_time = 15; // delay between servo move increments

int smin = 125; // minimum position, should be set above servo's hard-stop
int smax = 575; // maximum position, should be set above servo's hard-stop
int default_pos = 350; // default position to initialize to.  350 is center

// number of servos initialized
int num_servos = 3; 
// Last known locations of servos
int lasts [3] = { default_pos, default_pos, default_pos };
// Target locations of servos
int targets [3] = { default_pos, default_pos, default_pos };
// The amount of degrees to increment each servo at a time
int increment = 5;


void setup() {
  // drastically reduce Serial.readStringUntil time
  Serial.setTimeout(250); 
  // start Serial protocal
  Serial.begin(9600);
  Serial.println("Initializing.");
  pwm.begin();
  // Analog servos run at ~60 Hz updates
  pwm.setPWMFreq(60);  

  // Set servos to a default position
  // (mainly so they begin knowing where they are located)
  for (servo = 0; servo < num_servos; servo += 1) {
    Serial.println(servo);
    pwm.setPWM(servo, 0, default_pos);
    // These could be big direct moves so they can require longer
    // delay times
    delay(250);
  }
}


// The main loop.  Action is triggered when a message is sent
// over the Serial protocol
void loop() {
  if (Serial.available()) {
    message = Serial.readStringUntil('\n');
    Serial.println(message);
    moveServos(message);
  }
}


// Function for updating all the servos to target positions
void moveServos(const String& message) {
  // How many servos are being controlled in this message?
  int num_message_servos = message.length() / 3;

  // Parse message and set position targets for each servo
  int i = 0;
  for (i = 0; i < num_message_servos; i++) {
    targets[i] = message.substring(i * 3, (i * 3) + 3).toInt();
    Serial.println(targets[i]);
  }

  // Check how close we are to the targets
  int diff = 0;
  for (i = 0; i < num_message_servos; i++) {
    // If the command is invalid, do nothing
    if (targets[i] < smin || targets[i] > smax) {
      targets[i] = lasts[i];
    }
    diff += abs(lasts[i] - targets[i]);
  }

  
  int next = 0; // var for storing next position int
  int gap = 0;  // var for storing gap between current pos and target

  // Until the servos' last positions are target positions
  // update their positions by steps of 'increment'
  while (diff > 0) {
    diff = 0;
    for (servo = 0; servo < num_message_servos; servo += 1) {
      if (targets[servo] != lasts[servo]) {
        if (targets[servo] > lasts[servo]) {
          gap = targets[servo] - lasts[servo];
          next = lasts[servo] += min(increment, gap);
        }
        else if (targets[servo] < lasts[servo] && targets[servo] >= smin) {
          gap =  lasts[servo] - targets[servo];
          next = lasts[servo] -= min(increment, gap);
        }
        // Move servo to next position (should be <= increment)
        pwm.setPWM(servo, 0, next);
        // Delay to give it some time to move before processing next servo
        delay(delay_time);
        // Set last position to where we know the servo is now
        lasts[servo] = next;
        // Update the total difference between targets and current positions
        diff += abs(lasts[servo] - targets[servo]);
      }
    }
  }
}
