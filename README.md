# Twin Dragons

*An NES Platformer Written In [Millfork](https://github.com/KarolS/millfork)*

![Twin Dragons Gameplay](https://raw.githubusercontent.com/Garydos/twin-dragons-nes/master/res/twin_dragons.gif)

---

## Building

Run any of the `.bat` files to compile.  All binaries are placed in the
`bin` directory.

## Editing Levels

Levels are edited using Tiled.  The `.tmx` files for each level are stored in the `./src/levels/data` directory.

In order to export the maps, install the script located in the `tiled_plugin` directory and then export the level as a `.meta` file.
* Levels must be a multiple of `16` tiles in width, and exactly `15` tiles in height. 
* All levels must also use `metatiles.png` as their tilesheet.

All levels must also have their own `.mfk` file.  See `level0.mfk` for details.

## Adding Enemies

TODO

## Adding Frames/Animations

TODO

## Licensing
* Some artwork in this project was originally made by [surt](https://opengameart.org/content/twin-dragons) and is distributed here under a CC-BY 3.0 license.
* All code (except famitone5.0) is released under a zlib license (see LICENSE). For famitone5.0, see license.txt in the famitone5 directory