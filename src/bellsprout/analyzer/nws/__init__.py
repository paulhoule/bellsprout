from pathlib import Path

import imageio

src = Path.home() / "radar/Conus/RadarImg"
infiles = sorted(src.glob("*.gif"))

with imageio.get_writer(
        str(Path.home() / "radar/processed/northeast.avi"),
        mode='I',fps=10) as writer:
    for file in infiles:
        content = imageio.imread(str(file))
        writer.append_data(content)
