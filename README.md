# Dynamic Sketch Recognizer

This system is able to recognize items drawn on a touchscreen.

The dataset has been gathered through the use of the [touch-recorder](https://github.com/LucaMoschella/touch-recorder) android application.
The information recorded allows to reconstruct exactly how the drawing was done and to perform a dynamic analysis of the images.

| ![pesce2d](/docs/pesce2d.gif)             | ![sole2d](/docs/sole2d.gif)             |
| ----------------------------------------- | --------------------------------------- |
| ![pesce3d](/docs/pesce3d.gif)             | ![sole3d](/docs/sole3d.gif)             |
| ![pesce3ddecomp](/docs/pesce3ddecomp.gif) | ![sole3ddecomp](/docs/sole3ddecomp.gif) |

We have gathered a dataset on 61 pseudo-random objects and a MINST-like dataset of numbers.

The performance of the system on the MINST-like dataset are very encouraging:

![prfs_matrix](/docs/prfs.png)
___
![confusion_matrix](/docs/confusion.png)
___
![cmc_curve](/docs/cmc.png)
___
