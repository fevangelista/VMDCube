import re
import os


def hex_to_rgb(hex_color):
    """Convert a hex color string to RGB format."""
    if not isinstance(hex_color, str):
        raise ValueError("Invalid hex color")
    hex_color = hex_color.lstrip("#")
    if len(hex_color) != 6:
        raise ValueError("Invalid hex color")
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0
    return (r, g, b)


def parse_rgb_hex(color):
    """Convert a color specification to RGB format."""
    if isinstance(color, str) and color.startswith("#"):
        rgb = hex_to_rgb(color)
    elif isinstance(color, (tuple, list)):
        rgb = (
            color[0] / 255.0,
            color[1] / 255.0,
            color[2] / 255.0,
        )
    else:
        raise ValueError("Invalid color specification for colors")
    return rgb


def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file
    return None


def multigsub(subs, string):
    for k, v in subs.items():
        string = re.sub(k, v, string)
    return string
