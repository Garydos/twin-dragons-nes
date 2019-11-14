# Famitone5.0 Binary Build

This is a version of famitone5 with extra scripts for creating binary blobs usable with other NES toolchains.
For making binary versions of song data as well to work with this binary version of famitone5, see the `README.md` 
file in the `text2data` directory.

# Binary blob compiled with the default options `(DPCM samples @ $FC00, Famitone5 itself @ $C000)` is provided in the `bin` directory
### DON'T FORGET TO CHECK `famitone5.info` FOR THE ADDRESS OF EACH FUNCTION IF YOU CHANGE THE BINARY TO RESIDE IN A DIFFERENT LOCATION IN ROM !!!

## Build Requirements

The scripts used to build the binary files expect the `cc65` toolchain to be accessible to your system.

Install `cc65`, then either add the `cc65\bin` folder to your `PATH` variable,
or edit the scripts to use the full path to your `ca65` and `cl65` executables, i.e.
change `ca65` to `C:\cc65\bin\ca65.exe` and `ld65` to `C:\cc65\bin\ld65.exe`,
and do that for both `make.bat` files.



### Building `famitone5.bin`

Run make.bat to build `famitone5.bin`.  Resulting `famitone5.bin` and `famitone5.info` files are placed 
in the `bin` directory.

## Using the Famitone5 Binary Blob

To use `famitone5.bin` in a project, simply use your preferred toolchain to place `famitone5.bin` at the
location in ROM that was specified when building it.  It is recommended to have a dedicated bank for music data, so 
normally `famitone5.bin` is placed either at `$8000` or `$C000` in whatever bank you choose.

## Converting Famitracker Songs to Binary Format for Use with `famitone5.bin` (Getting Songs to Play)
Read `original_readme.txt`, `usage.txt`, `internal.txt`, and `warning.txt` for info on how to make songs in
Famitracker that will work with Famitone5.  Read the `README.md` file in `text2data` for more info on how
to convert the Famitracker module into a binary format compatible with Famitone5.