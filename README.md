#Video Subtitle renamer

Simple script for renaming video and subtitle files in _current_ directory. It renames video and subtitle files using the same format, removes unnecessary parts of file names as format, resolution, etc., keeping only actual movie/TV show name with season/episode information, resulting in clean names and automatic pairing of video and subtitle files in video players.

#### Available options

+ `-s %value%, --separator %value%` - uses `%value%` as a separator between words when renaming files, `-` is being used as a default separator
+ `-r, --recursive` - renames files recursively also in child directories
+ `-i, --interactive` - confirmation is required before each file gets renamed
+ `--testing` - no files are renamed, only text output is shown

### Usage

Place the script to the directory where you want to rename files, then run

```
python videoSubtitleRenamer.py [options]
```

For easy usage when you want to run the script for multiple different directories, place the script anywhere in your system and make it executable by running

```
chmod +x videoSubtitleRenamer.py
```

Then make a symbolic link from that file to some directory from your `PATH` (i.e. `bin/` in your home directory)

```
ln -s /path/to/videoSubtitleRenamer.py /path/to/dir/from/PATH
```

Now you will be able to execute the script from any directory by `cd` to that directory and running `videoSubtitleRenamer.py [options]`

#### Examples

`videoSubtitleRenamer.py` - base mode - running only for files in current directory, non-interactive, dash being used as a separator

`videoSubtitleRenamer.py -i -s .` - running in interactive mode with `.` being used as separator between words

`videoSubtitleRenamer.py -r --testing` - running in recursive and testing mode (files don't get renamed)