# Converting Famitracker Songs to Binary Format for Use with `Famitone2.bin` (Getting Songs to Play)
Once you have a Famitone2 compatible song or set of songs, use Famitracker
to export it/them as a `.txt` file (in Famitracker: `File->Export Text...`).  Next, place your `song.txt` file
in the `text2data` directory.  Run `make_song.bat` with your `song.txt` file as a parameter,
In windows drag `song.txt` over `make_song.bat` to run `make_song.bat` with `song.txt` as a parameter.  You can also do this
from the command line with the command `.\make_song.bat song.txt`.

Enter your build options when prompted, and then you'll
have either one or two files, `song.bin` and `song.dmc`.  `song.bin` is your song data, while `song.dmc` is your
song's DPCM samples, so if you don't have any DPCM samples in your song, it won't exist.  Move those
resulting files over to your project, insert them into your ROM at the place you specified when compiling the song,
and they should be ready to go.