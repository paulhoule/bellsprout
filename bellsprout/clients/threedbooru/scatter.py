"""
Early on when accumulating results from 3dbooru I set things up so that everything went in one big directory.

This winds up with about 600,000 HTML files.  Back in the bad old days,  searching for files by name required
a linear search which would have painful effects.

Even though most filesystems have indexes to speed up directory lookups I have still seen systems become
slow and unstable when there is a huge directory.  In fact,  I've seen some that never quite worked right
the same again.

I think this is happening now so I am going to split up that huge directory with this script

"""

from pathlib import Path
from os.path import expanduser
from shutil import copyfile

HOME = Path(expanduser("~"))
SOURCE = HOME / "3dbooru"
DESTINATION = HOME / "4dbooru"

# for outer in range(0,100):
#     print(f"Creating directory {outer*100}")
#
#     (DESTINATION / str(outer*100)).mkdir()
#     for inner in range(0,100):
#         (DESTINATION / str(outer*100) / str(outer*100+inner)).mkdir()

#
# I am not so sure what will happen with iterdir if we are moving files out of the directory so I am
# putting them in this list
#

files = list(SOURCE.iterdir())
idx = 0
for f in files:
    (number, extension) = str(f.name).split(".", maxsplit=1)
    number = int (number)
    last4 = number % 10000
    last2 = last4 % 100
    hundreds = last4 - last2
    copyfile(SOURCE / f.name, DESTINATION / str(hundreds) / str(last4) / f.name)
    idx += 1
    if not (idx % 1000):
        print("Copied {idx} files")

