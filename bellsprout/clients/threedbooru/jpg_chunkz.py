from os import SEEK_CUR
from pathlib import Path

filename = Path("/Users/paul/Downloads") / "90c8fe473f309da9a38562300047fb6c.jpg"

with open(filename,"rb") as FILE:
    if [ 0xff , 0xd8 ] != list(FILE.read(2)):
        raise ValueError("Invalid marker at beginning")

    position = 2
    while True:
        [ ff, marker_number ] = list(FILE.read(2))
        if ff != 0xff:
            raise ValueError(f"Marker Start Code Not Found at {position}  got {ff:#0x} instead")

        if marker_number == 0xd8:
            raise ValueError("Cannot have start marker in middle of sequence")

        if marker_number == 0xd9:
            print("Found end marker!")
            break

        if marker_number in {0xd0,0xd1,0xd2,0xd3,0xd4,0xd5,0xd6,0xd7}:
            marker_size = 2
        else:
            [msb, lsb] = list(FILE.read(2))
            marker_size = (msb << 8) + lsb

        print(f"Chunk type {marker_number:#0x} at position {position} with size {marker_size-2}")
        position = FILE.seek(marker_size-2,SEEK_CUR)

        last_result = b' '
        if marker_number in {0xd0,0xd1,0xd2,0xd3,0xd4,0xd5,0xd6,0xd7,0xda}:
            while True:
                this_result = FILE.read(1)
                if this_result == None:
                    raise ValueError("Caught exception in scan data")
                if this_result[0] != 0x00 and last_result[0] == 0xff:
                    break
                last_result = this_result

            old_position = position
            position = FILE.seek(-2,SEEK_CUR)
            print(f"** skipped {position-old_position} bytes of scan data ** ")



