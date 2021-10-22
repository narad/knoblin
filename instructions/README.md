# Instructions

Things you will need to use robo-knobs:
- Servos

  here are some useful servos
  
- Arduino
- Servo Controller
- External Power Supply
- USB MIDI Interface


## Servos

### 180 Degree Servos

These are some of the most readily available and cheapest options out there, including models like Tower Pro MG90S.  These have a 5mm shaft.  The disadvantages here is that I have found the gears to slip a bit, which over the course of hundreds of changes can create slightly unreliable readings.

### 270 Degree Servos

- [Smraza Servo Motor Digital 20kg](https://www.amazon.co.jp/gp/product/B087D1LWB3/ref=ppx_yo_dt_b_asin_title_o07_s00?ie=UTF8&psc=1)

Most of the 3D print parts and instructions will assume the use of these heavier duty Smraza servos.  In comparison to the Tower Pros, I find the gearing is more consistent and there is a more useful immediate torque for fast and fine knob adjustments.  The disadvantages are that they are a bit more expensive, and very power -- capable of snapping a typical pot shaft (I have witnessed firsthand!).  These have a 5.9mm (25T) shaft diameter.  For the rail model supports, the rails must support side mounts which are 48mm apart and fit a body 40.5mm long.

### 360 Degree Servos / Stepper Motors

I have experimented with 360 degree servos, but control of 360 servos operates in an entirely different way (from an Arduino p
