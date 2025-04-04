from re import search

from subprocess import call
from datetime import datetime
from glob import glob
from os import listdir, environ, getcwd, devnull, chdir
from os.path import isfile, join

from dataclasses import dataclass, field

from vmdcube.utils import (
    hex_to_rgb,
    parse_rgb_hex,
    which,
    multigsub,
)

from vmdcube.scripts import (
    vmd_script,
    vmd_script_surface,
    vmd_script_interactive,
    vmd_script_render,
    vmd_script_lights,
)

from vmdcube.materials import set_material


@dataclass
class VMDCube:
    """
    Class to generate VMD scripts for visualizing cube files."

    This class provides methods to set up the VMD environment, find cube files,
    generate VMD scripts for isosurface visualization, and optionally create
    montages of the generated images.
    It also includes properties for customizing the appearance of the generated
    images, such as rotation angles, translation values, material properties,
    and image dimensions.
    It uses the VMD software for molecular visualization and requires VMD to be
    installed and accessible in the system path.
    The class provides methods to run the VMD script and display the generated
    images in a Jupyter notebook.
    It also includes a method to create a montage of the generated images using
    the 'montage' command-line tool.
    The class is designed to be used in a command-line environment or within
    a Jupyter notebook.

    Example usage:
    ```python
        from vmdcube import VMDCube
        # Create an instance of VMDCube
        vmd = VMDCube()
        # Set properties for the visualization
        vmd.cubedir = "path/to/cube/files"
        vmd.isovalues = [0.05, -0.05]
        vmd.colors = ["#FF0000", "#00FF00"]

        # Run the VMD script to generate the visualization
        vmd.run()
    ```

    Attributes:
        default_path (str): Default path for cube files.
        cubedir (str): Directory containing cube files.
        interactive (bool): If True, run VMD in interactive mode.
        verbose (bool): If True, print detailed information.
        vmdpath (str): Path to the VMD executable.
        vmd_script_name (str): Name of the VMD script file.
        isovalues (list[float]): List of isovalues for isosurface generation.
        colors (list[int]): List of colors for isosurfaces.
        isovalue_cutoff (float): Isovalue cutoff for surface generation.
        rx, ry, rz (float): Rotation angles around x, y, and z axes.
        tx, ty, tz (float): Translation values along x, y, and z axes.
        ambient, diffuse, shininess, opacity (float): Material properties.
        width, height (int): Dimensions of the output image.
        scale (float): Scale factor for the image.
        show_width, show_height (float): Dimensions for displaying images.
        montage (bool): If True, combine images into a montage.
        fontsize (int): Font size for labels.
        label_mos (bool): If True, label MOs in the output images.
    """

    # general options
    default_path: str = getcwd()
    cubedir: str = "."
    cubefiles: list[str] = field(default_factory=list)
    interactive: bool = False
    verbose: bool = False

    # vmd options
    vmdpath: str = None
    vmd_script_name: str = "script.vmd"

    # isovalue and color
    default_isovalues: list[float] = field(default_factory=lambda: [0.05, -0.05])
    positive_color: int = 3
    negative_color: int = 23
    isovalues: list[float] = None
    colors: list[int] = None
    isovalue_cutoff: float = 1.0e-5
    background_color = None
    transparent: bool = False

    # rotation angles
    rx: float = 30.0
    ry: float = 40.0
    rz: float = 15.0

    # translation
    tx: float = 0.0
    ty: float = 0.0
    tz: float = 0.0

    # material type
    material_id: str = "default"

    # these values are set in the __post_init__ method by calling set_material
    ambient: float = field(init=False)
    diffuse: float = field(init=False)
    mirror: float = field(init=False)
    opacity: float = field(init=False)
    outline: float = field(init=False)
    outlinewidth: float = field(init=False)
    shininess: float = field(init=False)
    specular: float = field(init=False)
    transmode: int = field(init=False)

    # lighting options
    aoambient: float = 0.5
    aodirect: float = 0.5
    ambientocclusion: str = "off"
    shadows: str = "off"
    depthcue: str = "off"

    # rendering options
    width: int = 300
    height: int = 300
    scale: float = 1.0
    show_width: float = 7
    show_height: float = 7

    # other options
    montage: bool = False
    fontsize: int = 20
    label_mos: bool = True

    def __post_init__(self):
        set_material(self, "default")

    @property
    def scheme(self):
        return self.scheme

    @scheme.setter
    def scheme(self, value):
        if isinstance(value, str):
            scheme = value.lower().strip()
            if scheme == "national":
                self.colors = [23, 30]
            elif scheme == "silver":
                self.colors = [2, 8]
            elif scheme == "bright":
                self.colors = [32, 22]
            elif scheme == "electron":
                self.colors = [13, 12]
            else:
                raise ValueError(f"Unknown scheme: {value}")
        elif isinstance(value, (tuple, list)):
            if len(value) != 2:
                raise ValueError(
                    "Color scheme tuple/list must have exactly 2 elements."
                )
            self.colors = list(value)
        else:
            raise ValueError("Invalid type for scheme, expected str or tuple/list.")

    @property
    def material(self):
        return self.material

    @material.setter
    def material(self, value):
        if isinstance(value, str):
            mat = value.lower().strip()
            set_material(self, mat)

    def run(self):
        self.find_vmd()
        cube_files = self.find_cubes()
        self.make_script(cube_files)
        self.run_vmd()
        self.remove_background(cube_files) if self.transparent else None
        self.call_montage(cube_files) if self.montage else None

    def find_vmd(self):
        if environ.get("VMDPATH"):
            vmdpath = environ["VMDPATH"]
            vmdpath = multigsub({" ": r"\ "}, vmdpath)
            self.vmdpath = vmdpath
        else:
            raise ValueError(
                "\n\nvmdcube could not find the VMD executable."
                "\n\nTo fix this issue, check the following:"
                "\n1) VMD is installed."
                "\n3) The VMDPATH variable in your shell profile (e.g., .bashrc)"
                "\n   For example:\n"
                r"   export VMDPATH=/Applications/VMD 1.9.4a55-arm64-Rev11.app/Contents/vmd/vmd_MACOSXARM64\n"
            )

    def find_cubes(self):
        # Check if the cubefiles attribute is set. If yes, check that all files exist
        if self.cubefiles:
            for f in self.cubefiles:
                if not isfile(f):
                    raise ValueError(f"File {f} does not exist.")
            return sorted(self.cubefiles)

        # Find all the cube files in a given directory
        sorted_files = sorted([f for f in glob(join(self.cubedir, "*.cube"))])

        # if no cube files are found, exit
        if len(sorted_files) == 0:
            print("No cube files found in %s" % self.cubedir)

        return sorted_files

    def get_isovalues(self, filename):
        # If isovalues is not provided, try to read it from the cube file.
        if self.isovalues is not None:
            return self.isovalues
        else:
            # Assign a fallback value if isovalues is not contained in the cube file.
            isovalues = [0.05, -0.05]
            with open(filename, "r") as file:
                file.readline()  # ignore line 1
                l2 = file.readline()
                m = search(
                    r"density: \(([-+]?[0-9]*\.?[0-9]+),([-+]?[0-9]*\.?[0-9]+)\)",
                    l2,
                )
                if m:
                    isovalues[0] = float(m.group(1))
                    isovalues[1] = float(m.group(2))
        return isovalues

    def parse_color(self, color, index):
        # If colors is numeric, use it directly.
        if isinstance(color, (int, float)):
            color_index = color
            color_def_cmd = ""
        else:
            # Process custom color: if hex string, convert; if tuple/list, use directly.
            rgb = parse_rgb_hex(color)
            color_index = index
            color_def_cmd = f"color change rgb {index} {rgb[0]} {rgb[1]} {rgb[2]}\n"
        return color_index, color_def_cmd

    def get_colors(self, isovalues):
        """Determine the color to use to plot the isosurface."""
        # If colors is None, use default colors.
        colors = []
        color_def_cmd_list = []
        if self.colors is None:
            for index, isovalue in enumerate(isovalues):
                if isovalue > 0:
                    color_index, color_def_cmd = self.parse_color(
                        self.positive_color, index
                    )
                else:
                    color_index, color_def_cmd = self.parse_color(
                        self.negative_color, index
                    )
                colors.append(color_index)
                color_def_cmd_list.append(color_def_cmd)
        else:
            for index, color in enumerate(self.colors):
                color_index, color_def_cmd = self.parse_color(color, index)
                colors.append(color_index)
                color_def_cmd_list.append(color_def_cmd)

        return colors, "\n".join(color_def_cmd_list)

    def make_script(self, cube_files):
        """Create the VMD script for the cube files."""
        # Find the background color
        if self.background_color is None:
            self.background = (1.0, 1.0, 1.0)
        else:
            self.background = parse_rgb_hex(self.background_color)

        # Add lights and camera settings
        script = vmd_script_lights()

        # Loop through each cube file and generate the VMD script.
        for n, filename in enumerate(cube_files):
            cubenum = f"{n:03d}"
            cubefile = filename[:-5]

            # Define the image file name prefix.
            imgfile = cubefile
            parts = cubefile.split("_")
            if len(parts) == 4 and parts[0] == "./Psi":
                imgfile = f"{parts[0]}_{parts[1]}_{int(parts[2])}_{parts[3]}"

            # Build the head of the script using explicit parameters.
            script_head = vmd_script(cubefile, cubenum, self)

            # Get default isovalues and colors lists, and update from file if possible.
            isovalues = self.get_isovalues(filename)
            colors, color_def_cmd = self.get_colors(isovalues)

            if len(isovalues) != len(colors):
                raise ValueError(
                    "Number of isovalues and colors must match."
                    f"Got {len(isovalues)} isovalues and {len(colors)} colors."
                )
            else:
                (
                    print(f"Plotting {filename} with isosurface values {isovalues}")
                    if self.verbose
                    else None
                )

            # Build surface representations for each pair of isovalues and colors.
            script_surface = ""
            for value, color in zip(isovalues, colors):
                if abs(value) > float(self.isovalue_cutoff):
                    script_surface += color_def_cmd + vmd_script_surface(
                        self, cubenum, value, color
                    )
                else:
                    print(f" * Skipping isosurface with isocontour value {value}")

            # Choose interactive or render script.
            if self.interactive:
                script_render = vmd_script_interactive(cubenum)
            else:
                script_render = vmd_script_render(imgfile, cubenum)

            # Write the complete script for this cube file.
            script += script_head + "\n" + script_surface + "\n" + script_render

        if not self.interactive:
            script += "\n" + "quit"

        # Write the script to a file.
        with open(self.vmd_script_name, "w+") as vmd_script_file:
            vmd_script_file.write(
                "# VMD script generated by vmdcube.py\n"
                + datetime.now().strftime("%d-%B-%Y %H:%M:%S")
                + "\n"
            )
            vmd_script_file.write(script)

    def run_vmd(self):
        """Execute the VMD script."""
        FNULL = open(devnull, "w")
        if not self.interactive:
            call(
                f"{self.vmdpath} -dispdev text -e {self.vmd_script_name}",
                stdout=FNULL,
                shell=True,
            )
        else:
            call(
                f"{self.vmdpath} -e {self.vmd_script_name}",
                stdout=FNULL,
                shell=True,
            )

    def show(self):
        import glob
        from PIL import Image
        import matplotlib.pyplot as plt
        import ipywidgets as widgets
        from ipywidgets import HBox, VBox
        from IPython.display import display, clear_output

        # Get a sorted list of TGA files
        img_files = sorted(glob.glob(join(self.cubedir, "*.tga")))
        if not img_files:
            print("No image files found.")
            return

        # Create a dropdown widget with the image file names as options
        dropdown = widgets.Dropdown(
            options=img_files,
            value=img_files[0],
            description="",
            disabled=False,
        )

        # Create an output widget to display the image
        out = widgets.Output()

        # Create Previous and Next navigation buttons with rounded corners
        prev_button = widgets.Button(description="Previous")
        next_button = widgets.Button(description="Next")

        # Function to update image display
        def update_image():
            with out:
                clear_output(wait=True)
                img = Image.open(dropdown.value)
                plt.figure(figsize=(6, 6))
                plt.imshow(img)
                plt.axis("off")
                plt.show()

        # Dropdown change callback
        def on_dropdown_change(change):
            if change["name"] == "value":
                update_image()

        dropdown.observe(on_dropdown_change, names="value")

        # Previous button callback
        def on_prev_button_click(b):
            current_index = img_files.index(dropdown.value)
            new_index = (current_index - 1) % len(img_files)
            dropdown.value = img_files[new_index]

        prev_button.on_click(on_prev_button_click)

        # Next button callback
        def on_next_button_click(b):
            current_index = img_files.index(dropdown.value)
            new_index = (current_index + 1) % len(img_files)
            dropdown.value = img_files[new_index]

        next_button.on_click(on_next_button_click)

        # Arrange controls in a responsive layout using HBox and VBox
        controls = HBox([dropdown, prev_button, next_button])
        container = VBox([controls, out])
        container.layout = widgets.Layout(width="100%")  # make container responsive
        display(container)

        # Display the initial image
        update_image()

    def remove_background(self, cube_files):
        """
        Remove white background from an image and save it as PNG.
        """
        from PIL import Image

        # loop over the cube files (Path's)
        for f in cube_files:
            # replace the extension of f with .tga
            imgfile = f[:-5] + ".tga"
            print(f"Removing background from {imgfile}") if self.verbose else None

            # Open image
            img = Image.open(imgfile).convert("RGBA")

            # Choose the color to make transparent (e.g. white)
            target_color = (255, 255, 255)  # RGB for white
            tolerance = 10  # Allow small differences from target

            # Process each pixel
            datas = img.getdata()
            new_data = []

            for item in datas:
                r, g, b, a = item
                if (
                    abs(r - target_color[0]) < tolerance
                    and abs(g - target_color[1]) < tolerance
                    and abs(b - target_color[2]) < tolerance
                ):
                    new_data.append((r, g, b, 0))  # Make transparent
                else:
                    new_data.append(item)

            # Save new image
            img.putdata(new_data)
            img.save(imgfile)

    def call_montage(self, cube_files):
        # Optionally, combine all figures into one image using montage
        montage_exe = which("montage")
        if montage_exe is None:
            raise RuntimeError(
                "Montage is not installed. Please install ImageMagick to use this feature."
            )

        alpha_mos = [f"{f[:-5]}.tga" for f in cube_files if "Psi_a" in f]
        beta_mos = [f"{f[:-5]}.tga" for f in cube_files if "Psi_b" in f]
        densities = [f"{f[:-5]}.tga" for f in cube_files if "D" in f]
        basis_functions = [f"{f[:-5]}.tga" for f in cube_files if "Phi" in f]

        chdir(self.cubedir)

        # Sort the MOs by the orbital number
        sorted_mos = []
        for set in [alpha_mos, beta_mos]:
            sorted_set = sorted([(int(s.split("_")[2]), s) for s in set])
            sorted_mos.append([s[1] for s in sorted_set])

        # Add labels
        if self.label_mos:
            for i in range(2):
                for f in sorted_mos[i]:
                    f_split = f.split("_")
                    label = f"{f_split[3][:-4]}\ \({f_split[2]}\)"
                    cmd = (
                        f"montage -pointsize {self.fontsize} -label {label} {f} "
                        f"-geometry '{self.width}x{self.height}+0+0>' {f}"
                    )
                    call(cmd, shell=True)

        # Combine together in one image
        if len(alpha_mos) > 0:
            call(
                (
                    f'{montage_exe} {" ".join(sorted_mos[0])} -geometry +2+2 AlphaMOs.tga'
                ),
                shell=True,
            )
        if len(beta_mos) > 0:
            call(
                (f'{montage_exe} {" ".join(sorted_mos[1])} -geometry +2+2 BetaMOs.tga'),
                shell=True,
            )
        if len(densities) > 0:
            call(
                (
                    "%s %s -geometry +2+2 Densities.tga"
                    % (montage_exe, " ".join(densities))
                ),
                shell=True,
            )
        if len(basis_functions) > 0:
            call(
                (
                    "%s %s -geometry +2+2 BasisFunctions.tga"
                    % (montage_exe, " ".join(basis_functions))
                ),
                shell=True,
            )
        chdir(self.default_path)
