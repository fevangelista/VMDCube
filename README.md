# VMDCube

![GitHub](https://img.shields.io/github/license/fevangelista/vmdcube)
![GitHub issues](https://img.shields.io/github/issues/fevangelista/vmdcube)
![GitHub pull requests](https://img.shields.io/github/issues-pr/fevangelista/vmdcube)
![GitHub last commit](https://img.shields.io/github/last-commit/fevangelista/vmdcube)
![GitHub contributors](https://img.shields.io/github/contributors/fevangelista/vmdcube)
![GitHub repo size](https://img.shields.io/github/repo-size/fevangelista/vmdcube)
![GitHub stars](https://img.shields.io/github/stars/fevangelista/vmdcube)
![GitHub forks](https://img.shields.io/github/forks/fevangelista/vmdcube)

## Description

A simple pip-installable Python module to generate pretty 3D visualizations of molecular orbitals like the one below:

<p align="center">
<img src="https://raw.githubusercontent.com/fevangelista/vmdcube/main/images/title.png" alt="Example of orbital rendered with VMDCube." width="450"/>
</p>

VMDCube is designed to work with <a href="https://www.ks.uiuc.edu/Research/vmd/">VMD (Visual Molecular Dynamics)</a> and can render isocountour surfaces saved in the standard cube file format. VMDCube can visualize molecular orbitals, electron density, and other volumetric data.

## Features

VMDCube can be used in Python scripts and Jupyter notebooks to render cube files. Here is an example of how to use it in Python:

```python
from vmdcube import VMDCube
vmd = VMDCube() # by default, render all cube files in the current directory
vmd.run()
```

The following showcases VMDCube's visualization capabilities in Jupyter notebooks:

<p align="center">
<img src="https://raw.githubusercontent.com/fevangelista/vmdcube/main/images/example.png" alt="Example use of VMDCube in Jupyter." width="450"/>
</p>

## Installation and setup

### VMDCube

VMDCube is available on PyPI and can be installed using pip:

```bash
pip install vmdcube
```

### VMD Path

VMDCube requires the environment variable `VMDPATH` to be set to the location of the VMD executable.

For example, if you’re using zsh and the VMD executable is `/Applications/VMD 1.9.4a55-arm64-Rev11.app/Contents/vmd/vmd_MACOSXARM64`, set `VMDPATH` to this value in your shell configuration file.
For example, for zsh add this line to your `~/.zshrc` file:

```bash
export VMDPATH=/Applications/VMD\ 1.9.4a55-arm64-Rev11.app/Contents/vmd/vmd_MACOSXARM64
```

After updating `~/.zshrc`, either restart your terminal or run the following so the change takes effect:

```bash
source ~/.zshrc
```

### VMD

VMDCube requires VMD to be installed on your system. You can download VMD from the official website: [VMD Download](https://www.ks.uiuc.edu/Research/vmd/).

## Installation from source

Clone the repository, then run:

```bash
git clone git@github.com:fevangelista/VMDCube.git
cd VMDCube
pip install -e .
```

## Tutorials

See [the VMDCube introductory tutorial](https://github.com/fevangelista/VMDCube/blob/main/tutorials/vmdcube_tutorial.ipynb) for how to use VMDCube in Jupyter notebooks and available rendering options.
