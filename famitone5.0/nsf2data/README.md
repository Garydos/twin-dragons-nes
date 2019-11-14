# Converting Famitracker SFX to Binary Format for Use with `famitone5.bin` (Getting SFX to Play)
Once you have a Famitone5 compatible set of sound effects, use Famitracker
to export them as a `.nsf` file (in Famitracker: `File->Create NSF...`).  Next, place your `sfx.nsf` file
in the `nsf2data` directory.  Run `make.bat` with your `sfx.nsf` file as a parameter,
**In windows, drag `song.txt` over `make.bat` to run `make.bat` with `song.txt` as a parameter**.  You can also do this
from the command line with the command `.\make.bat sfx.nsf`.

Enter your build options when prompted, and then you'll
have either one or two files, `sfx.bin` and `sfx.dmc`.  `sfx.bin` is your sfx data, while `sfx.dmc` is your
sfx's DPCM samples, so if you don't have any DPCM samples in your sfx, it won't exist.  Move those
resulting files over to your project, insert them into your ROM at the place you specified when compiling the sfx,
and they should be ready to go.