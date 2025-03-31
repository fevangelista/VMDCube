def vmd_script(cubefile, cubenum, vmdcube):
    """Generate a VMD script to plot MOs from cube files."""
    return f"""
#
# Plot the cube file {cubefile}.cube
#

# Load the molecule and change the atom style
mol load cube {cubefile}.cube
mol modcolor 0 {cubenum} Element
mol modstyle 0 {cubenum} Licorice 0.110000 10.000000 10.000000

# Define the material for rendering atoms
material change ambient      Opaque 0.310000
material change diffuse      Opaque 0.720000
material change specular     Opaque 0.500000
material change shininess    Opaque 0.480000
material change opacity      Opaque 1.000000
material change outline      Opaque 0.000000
material change outlinewidth Opaque 0.000000
material change transmode    Opaque 0.000000
material change specular     Opaque 0.750000

# Define the material for rendering isosurfaces
material change ambient      EdgyShiny {vmdcube.ambient}
material change diffuse      EdgyShiny {vmdcube.diffuse}
material change mirror       EdgyShiny {vmdcube.mirror}
material change opacity      EdgyShiny {vmdcube.opacity}
material change outline      EdgyShiny {vmdcube.outline}
material change outlinewidth EdgyShiny {vmdcube.outlinewidth}
material change shininess    EdgyShiny {vmdcube.shininess}
material change specular     EdgyShiny {vmdcube.specular}
material change transmode    EdgyShiny {vmdcube.transmode}

# Customize atom colors
color Element C silver
color Element H white

# Rotate and translate the molecule
rotate x by {vmdcube.rx}
rotate y by {vmdcube.ry}
rotate z by {vmdcube.rz}
translate by {vmdcube.tx} {vmdcube.ty} {vmdcube.tz}
scale by {vmdcube.scale}

# Eliminate the axis and perfect the view
axes location off
display projection orthographic
display ambientocclusion {vmdcube.ambientocclusion}
display shadows {vmdcube.shadows}
display aoambient {vmdcube.aoambient}
display aodirect {vmdcube.aodirect}
display rendermode Tachyon
display depthcue {vmdcube.depthcue}
display resize {vmdcube.width} {vmdcube.height}
# Set the background color
color change rgb 1000 {vmdcube.background[0]} {vmdcube.background[1]} {vmdcube.background[2]}
color Display Background 1000
"""


def vmd_script_surface(vmdcube, cubenum, isovalue, color):
    """Generate a VMD script to plot an isosurface from a cube file."""
    return f"""#
# Add a surface
mol color ColorID {color}
mol representation Isosurface {isovalue} 0 0 0 1 1
mol selection all
mol material EdgyShiny
mol addrep {cubenum}
"""


def vmd_script_interactive(cubenum):
    """Generate a VMD script to run in interactive mode."""
    return f"""#
# Disable rendering
mol off {cubenum}
"""


def vmd_script_render(imgfile, cubenum):
    """Generate a VMD script to render the molecule."""
    return f"""
# Render
render TachyonInternal {imgfile}.tga
mol delete {cubenum}
"""


def vmd_script_lights():
    """Generate a VMD script to rotate the molecule."""
    return f"""
light 1 off
light 0 rot y  30.0
light 0 rot x -30.0
"""
