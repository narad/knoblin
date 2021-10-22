# robo-knob

Robo-knob is a library of code, instructions, and model specifications for automated control of the knobs on musical devices, especially those found on guitar amplifiers and effects pedals.  

While originally developed as a way of performing large-scale data gathering from musical devices, there are probably lots of other fun uses for it!  Some ideas that spring to mind are preset changes on analog equipment, changing device settings based on what is being played, changing timbre over the envelope of the notes being played, etc.)

Robo-knob is roughly partitioned into three sections:
- Material requirements, the basic components you'll need to buy to setup the interface
- 3D models, the adapters and mounts for connecting the controls to the music devices
- Code, for issuing the control commands to the device (a mix of Python and C++/Arduino)

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
