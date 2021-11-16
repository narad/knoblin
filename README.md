# Knoblin

<p align="center">
<img src="https://github.com/narad/knoblin/blob/main/images/knoblin.png" width=500>
</p>

The Knoblin (KNOB controller and LINkages) is a library of code, instructions, and model specifications for MIDI control of the knobs on musical devices, especially those found on guitar amplifiers and effects pedals.  


While originally developed as a way of performing large-scale data gathering from musical devices (for this [paper](https://github.com/narad/knoblin#Reference), there are probably lots of other fun uses for it!  Some ideas that spring to mind are preset changes on analog equipment, changing device parameters based on what is being played, changing them over the duration of the envelope of the notes being played, etc.)

Knoblin is roughly partitioned into three sections:
- [Material requirements and instructions](https://github.com/narad/robo-knob/tree/main/instructions#readme), the basic components you'll need to buy to setup the interface
- [3D models](https://github.com/narad/robo-knob/tree/main/models#readme), the adapters and mounts for connecting the controls to the music devices
- [Code](https://github.com/narad/robo-knob/tree/main/knoblin#readme), for issuing the control commands to the device (a mix of Python and C++/Arduino)

<p align="center">
<img src="https://lh3.googleusercontent.com/pw/AM-JKLUU6OLRZBpZZ1fSlGHTyd6Nc_3qeryEBcGChPrbRdNDIDkH2HIPs7jZ8heEMR8PKg6PJMBVfRFL-BTs9V7O7Xoz1YdXrvX4BglB_NvO-Hf2uskDHJ_7cejyRkgrizWHWm1mQj7DkOdWZwco03XfZJbG=w1695-h1736-no" alt="drawing" width="400"/>
</p>

Watch/Listen to Knoblin in action in the [YouTube Demo](https://youtu.be/dsk65mj1pfU)

### Overall Design

<p align="center">
<img src="https://github.com/narad/robo-knob/blob/main/images/knoblin-design.png?raw=true" width="500">
</p>

### Reference

If using Knoblin code in academic work, please cite the [paper](https://www.dafx.de/paper-archive/details.php?id=G8gchE7K8Itm8VPTGRtYyA) it was developed for:

```
@article{narad2021ampspace,
  title = {Amp-Space: A Large-scale Dataset for Fine-grained Timbre Transformation},
  author = {Naradowsky, Jason},
  journal = {Proceedings of the 24th International Conference on Digital Audio Effects (DAFx-21), Vienna, Austria},
  year = {2021}
}
```

### Acknowledgements

Michael Karsay's [Terrorbot](http://trigonometrie.bplaced.net/blog/terrorbot/) project was a great inspiration and proof-of-concept that led me down the Arduino path, as was Thomas Töngi's [geckotool](https://geckotool.com/) project.  I learned a lot in a little time thanks to help from the 3D printing community.  Many thanks to Josef Prusa and [The 3D Printing Professor](https://www.youtube.com/channel/UCJk5KVaJVBEEl_jP5gKjoDw) -- who knew printing effective and accurate LEGO-compatible blocks was such a complicated topic!  Thanks to @Raspencil for The Knoblin graphic, and Mike Wirth, Victor Bolivar, Don Patino, Guilhem, and Vectors Point for artwork used in diagrams.

### Disclaimer

While I've worked to implement reasonable safeguards, there are always risks when using code and automation to interact with objects in the real world.  This is especially true when the code has been tested in a very particular environment, on a very particular set of devices.  The servos used in this project are more than capable of generating enough torque to damage things, so use the code with caution, and exercise care when calibrating the connections between servos and knobs.  I cannot be held liable for damages that arise from using this code, correctly or otherwise.  Use at your own risk.
