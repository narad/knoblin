# 3D models

The main considerations to these parts is that they would be:
- easily printable even with budget printetrs
- flexible enough to be used on a variety of gear, including both pedals (vertical knob orientation) and amps (often horizontal knob orientation).

## Servo-Pot Coupling Shaft

The first physical control problem to solve is attaching a servo to a knob's potentiometer

One option is to simply use rigid couplers like these.  What's wrong with this approach?  Nothing, if nothing goes wrong.  Otherwise, it's good to have a point of failure that's not on the servo (sithe metal-geared servos I recommend using are not likely to be the weakest link in the chain) and not on your possibly expensive and difficult to repair gear!  To solve this problem (and a few others) I've designed a simple shaft with beveled caps which can attach to the recommended servos shafts and typical CTS-style pots.

<img src="https://github.com/narad/robo-knob/blob/main/models/images/shaft.png?raw=true" width="300">

This includes an M2-spec screw to tighten around the servo or pot shaft if necessary, though adding more filament to the shaft wall is probably recommended if using standard length M2 screws.

## Servo support rails

Now that the servos can be attached to the pedal/amp pots, the servo is capable of turning the knob, but only if held in place.  I designed the following rail for the Smraza 270 degree servos described [here](https://github.com/narad/robo-knob/tree/main/instructions#:~:text=use%20robo-knobs%3A-,Servos,-Servos%20are%20small).  The servos mount to a pair of rails, attaching with M2 or M3-sized bolts, and can be slid horizontally along the rail to match the spacing of a row of knobs.

<img src="https://github.com/narad/robo-knob/blob/main/models/images/rails.png?raw=true" width="600">

### Thinking in 3D

An issue sometimes arises when pedals have knobs are not arranged in a single row.  Often times this means it's not possible to place a second rail support without it physically interfering with the first.  In these cases the only way is up!  By thinking of servos as occupying different "levels" and positioning a second rail above the first, we can build more flexible configurations of servos to handle most of these situations.  Designing 3D printable scaffolds to support all the various knob arrangements would be nearly impossible, so instead I designed the rails to support LEGO-style mounts (using templates from [printablebricks](https://printablebricks.com/)).  LEGO is modular, standardized, widely available, and relatively cheap for this application, so it seemed like a well-suited solution.  

## Caps for Knobs

Attaching servos to pots usually makes the most sense since there is so much variety in the types of knobs, the knobs on many pedals are very close together, and knobs may also slip on the pot which can lead to incorrect control.  On the other hand, it can be a real pain to take knobs off and to align the coupling shafts properly, especially on amplifiers.  To make this a bit easier I've also design some "semi-universal" caps which can be used to attach coupling shafts directly to the knobs of amps which use Marshall/Fender style knobs.
