def set_material(vmdcube, material):
    if material == "default":
        default_material(vmdcube)
    elif material == "old":
        old_material(vmdcube)
    elif material == "glass":
        glass_materials(vmdcube)
    elif material == "shiny":
        shiny_material(vmdcube)
    else:
        raise ValueError("Invalid material type. Choose 'old' or 'default'.")
    vmdcube.material_id = material


def default_material(vmdcube):
    vmdcube.ambient = 0.6
    vmdcube.diffuse = 0.5
    vmdcube.mirror = 0.0
    vmdcube.opacity = 1.0
    vmdcube.outline = 0.0
    vmdcube.outlinewidth = 0.0
    vmdcube.shininess = 0.75
    vmdcube.specular = 0.96
    vmdcube.transmode = 0


def old_material(vmdcube):
    vmdcube.ambient = 0.31
    vmdcube.diffuse = 0.72
    vmdcube.mirror = 0.0
    vmdcube.opacity = 1.0
    vmdcube.outline = 0.76
    vmdcube.outlinewidth = 0.94
    vmdcube.shininess = 0.75
    vmdcube.specular = 0.96
    vmdcube.transmode = 0


def shiny_material(vmdcube):
    vmdcube.ambient = 0.15
    vmdcube.diffuse = 0.85
    vmdcube.mirror = 0.0
    vmdcube.opacity = 1.0
    vmdcube.outline = 0.0
    vmdcube.outlinewidth = 0.0
    vmdcube.shininess = 0.5
    vmdcube.specular = 0.2
    vmdcube.transmode = 0


def glass_materials(vmdcube):
    vmdcube.ambient = 0.04
    vmdcube.diffuse = 0.34
    vmdcube.mirror = 0.0
    vmdcube.specular = 1.0
    vmdcube.shininess = 1.0
    vmdcube.opacity = 0.1
    vmdcube.outline = 0.0
    vmdcube.outlinewidth = 0.0
    vmdcube.transmode = 1
