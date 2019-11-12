# Famitone2.0 Binary Build

This is a version of Famitone2 with extra scripts for creating binary blobs usable with other NES toolchains.
For making binary versions of song data as well to work with this binary version of Famitone2, see the `README.md` 
file in the `tools` directory.

# Binary blob compiled with the default options `(DPCM samples @ $FC00, Famitone2 itself @ $C000)` is provided in the `bin` directory
### DON'T FORGET TO CHECK `Famitone2.info` FOR THE ADDRESS OF EACH FUNCTION IF YOU CHANGE THE BINARY TO RESIDE IN A DIFFERENT LOCATION IN ROM !!!

## Build Requirements

The scripts used to build the binary files expect the `cc65` toolchain to be accessible to your system.

Install `cc65`, then either add the `cc65\bin` folder to your `PATH` variable,
or edit the scripts to use the full path to your `ca65` and `cl65` executables, i.e.
change `ca65` to `C:\cc65\bin\ca65.exe` and `ld65` to `C:\cc65\bin\ld65.exe`,
and do that for both `make.bat` files.



### Building `Famitone2.bin`

Run make.bat to build `Famitone2.bin`.  Resulting `Famitone2.bin` and `Famitone2.info` files are placed 
in the `bin` directory.

## Using the Famitone2 Binary Blob

To use `Famitone2.bin` in a project, simply use your preferred toolchain to place `Famitone2.bin` at the
location in ROM that was specified when building it.  It is recommended to have a dedicated bank for music data, so 
normally `Famitone2.bin` is placed either at `$8000` or `$C000` in whatever bank you choose.

## Converting Famitracker Songs to Binary Format for Use with `Famitone2.bin` (Getting Songs to Play)
Read the original `readme.txt` for info on how to make songs in
Famitracker that will work with Famitone2.  Read the `README.md` file in `text2data` for more info on how
to convert the Famitracker module into a binary format compatible with Famitone2.