# robo-knob

Robo-knob is a library of code, instructions, and model specifications for MIDI control of the knobs on musical devices, especially those found on guitar amplifiers and effects pedals.  

While originally developed as a way of performing large-scale data gathering from musical devices (for this [paper](https://github.com/narad/robo-knob/tree/main/readme#reference), there are probably lots of other fun uses for it!  Some ideas that spring to mind are preset changes on analog equipment, changing device parameters based on what is being played, changing them over the duration of the envelope of the notes being played, etc.)

Robo-knob is roughly partitioned into three sections:
- [Material requirements and instructions](https://github.com/narad/robo-knob/tree/main/instructions#readme), the basic components you'll need to buy to setup the interface
- [3D models](https://github.com/narad/robo-knob/tree/main/modelss#readme), the adapters and mounts for connecting the controls to the music devices
- [Code](https://github.com/narad/robo-knob/tree/main/knobs#readme), for issuing the control commands to the device (a mix of Python and C++/Arduino)

### Reference

If using robo-knob code in academic work, please cite the [paper](https://www.dafx.de/paper-archive/details.php?id=G8gchE7K8Itm8VPTGRtYyA) it was developed for:

```
@article{narad2021ampspace,
  title = {Amp-Space: A Large-scale Dataset for Fine-grained Timbre Transformation},
  author = {Naradowsky, Jason},
  journal = {Proceedings of the 24th International Conference on Digital Audio Effects (DAFx-21), Vienna, Austria},
  year = {2021}
}
```

### Disclaimer

While I've worked to implement reasonable safeguards, there are always risks when using code and automation to interact with objects in the real world.  This is especially true when the code has been tested in a very particular environment, on a very particular set of devices.  The servos used in this project are more than capable of generating enough torque to damage things, so use the code with caution, and exercise care when calibrating the connections between servos and knobs.
