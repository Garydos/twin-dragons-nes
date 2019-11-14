# Twin Dragons

*An NES Platformer Written In [Millfork](https://github.com/KarolS/millfork)*

![Twin Dragons Gameplay](https://raw.githubusercontent.com/Garydos/twin-dragons-nes/master/res/twin_dragons.gif)

---

## Building

Run `make.bat` to compile.  Make sure to edit `make.bat` to point to your Millfork installation before running it.

The resulting binaries are placed in the
`bin` directory.

### Editing Levels

Levels are edited using Tiled.  The `.tmx` files for each level are stored in the `./src/levels/data` directory.
You must install the python script located in the `tiled_plugin` directory in order to be able to export these maps.

To export a map, make sure the python plugin is installed, and then in Tiled you'll be able to click `File->Export` and see `*.meta` as one of the
"Save as type" options.  In order for the map to export properly, make sure it follows all of these rules:
* Levels must be a multiple of `16` tiles in width, and exactly `15` tiles in height. 
* All levels must use `metatiles.png` as their tilesheet.
* Tiles must be drawn on a tile layer named `Tiles`.  Enemy spawn objects must be placed on an object layer labeled `Enemies`.
* Enemy spawn objects must have the exact string `enemy_spawn` in their `Type` property.
* Enemy spawn objects must each have a custom property named `enemy_type`, and the value of that property determines what enemy spawns at that location,
i.e. a value of `0` in `enemy_type` will spawn a boomba in that location.
* There must only be one enemy spawn object per 16 pixel column.
* Currently the maximum amount of enemy spawns per level is `32`.  This can be changed by changing the size of the arrays found in `levels.mfk`

See `test.tmx` as an example map.


All levels must also have their own `.mfk` file which is then imported into the `levels.mfk` file.
Use `level0.mfk` as a template by copy-pasting its contents into your own `levelX.mfk` file and then replace all the data with your own level data.
Finally, go into `levels.mfk` and in the `load_level` function, add your level load function to the list of if statements like so:

```
    if level_num == 0 {
        load_level0()
    }
    if level_num == X {
        load_levelX()
    }
```

After this, you should be able to go to any existing level, change `next_level` to your new level's number, and it'll load your new level after completing that one.

### Adding Graphics

Graphics data (from now on referred to as the `CHRROM` code) is stored in the `./src/graphics/twin_dragons.chr` file.
To add new tiles/sprites, simply edit this file with the appropriate bits that represent your tile.
I recommend using [YY-CHR](https://www.romhacking.net/utilities/119/) to do this easily.

**Please Note:** ***The location of a tile in CHRROM determines its collidability***

Currently, these two functions in `.src/physics.mfk` determine the ranges for which tiles in CHRROM collide with movable objects:

```
bool is_collidable(byte tile) {
    if tile >= $C0 && tile < $FF {
        if tile == $F0 || tile == $F1 || tile == $F2 || tile == $F3 || 
            tile == $D4 || tile == $D5 || tile == $D6 || tile == $D7 {
            hit_spike = 1
        }
        return true
    }
    if tile >= $68 && tile <= $6B{
        touched_goal = 1
    }
    return false
}

inline void slope_check(byte tile) {
    if tile == $CA || tile == $C9 {
        on_slope = 2
    }
    else if tile == $CC || tile == $CF {
        on_slope = 1
    }
    else {
        on_slope = 0
    }
}
```

These functions label all tiles between `$C0` and `$FF` as collidable tiles.
Slopes are also detected through the tiles placed between `$C9,$CA,$CC` and `$CF`.


Make sure to edit these functions/ranges if you plan to change which tiles are collidable with the player/enemies.

### Adding/Defining Metatiles

Metatiles are 16x16 pixel tiles made up of 4 8x8 graphics tiles.

To add/define new metatiles, first make a new metatile in `src/graphics/metatiles.png`.  This is so that the metatile
shows up in maps that are edited using Tiled.  Make sure that the tiles that make up the metatile already exist within
CHRROM.

Next, define the new metatile's component tiles in the array located in `metatiles.mfk`.
At the bottom of the file, you'll find an array called `Metatiles`:

```
const array metatiles = [
			//Tile positions:
			//top-left	bot-left	top-right	bot-right
            $24,		$24,		$24,		$24,
            [ ... ]
            $68,        $6A,        $69,        $6B
            
]
```

The [...] represents already defined metatiles.  

Say we want to define a metatile that uses tile `$00` as its top-left tile,
`$01` as its bottom-left tile, `$02` as its top-right tile, and
`$03` as its bottom-right tile.


To define this metatile, simply add its four component tiles
to the end of the array like so:

```
const array metatiles = [
			//Tile positions:
			//top-left	bot-left	top-right	bot-right
            $24,		$24,		$24,		$24,
            [ ... ]
            $68,        $6A,        $69,        $6B,
            $00,        $01,        $02,        $03
            
]
```

Notice how this is an array, so every entry must have a comma after it except for the last entry.
Also note that this only applies if you're appending a new metatile to the end of your metatile list.
If you instead inserted a metatile in the middle of `metatiles.png`, then you need to find the correct
location within the array to insert its tiles.

Next, you need to edit the tiled python script supplied in the `tiled_plugin` directory.

Open up `metatile_nes.py` and you'll see at the top of the file is a dictionary named `tile_attrs`.
You must add the number of your new metatile and the palette that it uses to this dictionary.  If you are
appending a new metatile, then its metatile number is simply +1 of the second-to-last number in the dictionary.

For example, if we currently only have a single metatile defined, then `tile_attrs` looks like this:

```
#Which palette does each metatile use? Edit this to the appropriate palette
#number when making new metatiles (metatile_number : palette_number)
tile_attrs = {
    0:0,
    255:1
}
```

If we appended a metatile which uses the second palette (index 1), then we change the dictionary by adding one line:

```
#Which palette does each metatile use? Edit this to the appropriate palette
#number when making new metatiles (metatile_number : palette_number)
tile_attrs = {
    0:0,
    1:1,
    255:1
}
```

After this is done, re-install your newly modified python script to your `~/.tiled` directory to see the changes in Tiled.
If the new metatile you've added is a slope, don't forget to change the `slope_check` function in `physics.mfk` to have
it work properly in-game.

### Adding Frames/Animations

See `animation_structure.txt` for info on how animation data is structured.  By convention, all frame/animation data is placed at the bottom of `animation.mfk`.
Once you've got your frame/animation data ready, you need to add them to the functions `handle_current_anim` and `draw_current_frame` in `animation.mfk` in order to use them in-game.

For example, in `draw_current_frame`, if you have a new frame called `health_pickup_static_frame`, you can add it in like so:
```
    if frame_num == 0 {
        sprite_draw_frame(player_idle_frame.addr, x,y, mirroring)
    }
    if frame_num == X {
        sprite_draw_frame(health_pickup_static_frame.addr, x,y, mirroring)
    }
```
Where X is your new frame number that doesn't conflict with any other frame numbers.
Note that these frame numbers also define the frames represented by the frame numbers in animation data.

For adding animations in `handle_current_anim`, you do something similar:
```
    if current_anim->anim_num == 0 {
        anim_ptr = player_idle_anim.addr
    }
    if current_anim->anim_num == X {
        anim_ptr = health_pickup_static_anim.addr
    }
```
Where X is an animation number that doesn't conflict with other animation numbers.

When adding animations, it is best to add them to `handle_current_anim` and write the code to display the animation first before trying to completely fill out the animation data.  That way you'll be able to see how the animation looks like right away and adjust any errors visually.

### Adding Enemies

TODO

## Licensing
* Some artwork in this project was originally made by [surt](https://opengameart.org/content/twin-dragons) and is distributed here under a CC-BY 3.0 license.
* All code (except famitone2) is released under a zlib license (see LICENSE). For famitone2, see readme.txt in the famitone2 directory
* Music in the `famitone2` directory is made by [Shiru](https://shiru.untergrund.net/), all rights reserved to Shiru.
* All other music is made by Garydos and is released under a Creative Commons 4.0 BY license.