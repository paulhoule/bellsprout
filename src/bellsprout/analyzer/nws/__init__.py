from pathlib import Path

import imageio

src = Path.home() / "radar/Conus/RadarImg"
infiles = list(src.glob("*.gif"))

with imageio.get_writer(str(Path.home() / "northeast.gif"),mode='I') as writer:
    for file in infiles:
        content = imageio.imread(str(file))
        writer.append_data(content)
