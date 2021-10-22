# Instructions

Things you will need to use robo-knobs:
- [Servos](https://github.com/narad/robo-knob/blob/main/instructions/README.md#Servos)
- [Arduino](https://github.com/narad/robo-knob/blob/main/instructions/README.md#Arduino)
- [Servo Controller](https://github.com/narad/robo-knob/blob/main/instructions/README.md#Servo-Controller)
- [External Power Supply](https://github.com/narad/robo-knob/blob/main/instructions/README.md#external-power-supply)
- [USB MIDI Interface](https://github.com/narad/robo-knob/blob/main/instructions/README.md#usb-midi-interface)


## Servos

Servos are small motors, widely used in hobbyist robotics and RC cars.  They vary in terms of their operable range of rotation (notable examples are 180/270/360).  In robo-knob, the servos act as the method of physical motion driving control of the knobs.

### 180 Degree Servos

180 degrees servos can automate knob changes between values of approximately 3 to 8 on a Fender-style 1-10 knob, and therefore cover a lot of the usable range of the tone controls on many devices.  These servos are also some of the most readily available and cheapest options.  A standard recommendation is the [Tower Pro MG90S](https://www.amazon.com/Maxmoral-Upgraded-Digital-Vehicle-Helicopter/dp/B07NV476P7).     Most have a 5mm shaft, require a 5-6mm couple for most pots.  

### 270 Degree Servos

270 degrees covers the range of 

- [Smraza Servo Motor Digital 20kg](https://www.amazon.co.jp/gp/product/B087D1LWB3/ref=ppx_yo_dt_b_asin_title_o07_s00?ie=UTF8&psc=1)

Most of the 3D print parts and instructions will assume the use of these heavier duty Smraza servos.  In comparison to the Tower Pros, I find the gearing is more consistent and there is a more useful immediate torque for fast and fine knob adjustments.  The disadvantages are that they are a bit more expensive, and very power -- capable of snapping a typical pot shaft (I have witnessed firsthand!).  These have a 5.9mm (25T) shaft diameter.  For the rail model supports, the rails must support side mounts which are 48mm apart and fit a body 40.5mm long.

### 360 Degree Servos / Stepper Motors

I have experimented with 360 degree servos, but control of 360 servos operates in an entirely different way (from an Arduino p
The disadvantages here is that I have found the gears to slip a bit, which over the course of hundreds of changes can create slightly unreliable readings.

## Arduino

An Arduino unit is required for establishing the link between a computer and the servos (or the servo controller in this case) by hosting and executing simple command programs.  I recommend using a servo controller which will take the headache out of controlling > 2 servos simultaneously, and in this case, almost any Arduino unit is probably suitable.  Generally I recommend the [Uno releases](https://www.amazon.com/Arduino-A000066-ARDUINO-UNO-R3/dp/B008GRTSV6), or the [Elegoo Arduino starter kit](https://www.amazon.com/ELEGOO-Project-Tutorial-Controller-Projects/dp/B01D8KOZF4) which has lots of useful components and some other fun projects.

## Servo Controller

## External Power Supply

## USB MIDI Interface
