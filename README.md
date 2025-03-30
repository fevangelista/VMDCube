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

A simple pip-installable Python module to generate pretty 3D visualizations of molecular orbitals like this the one below:

<p align="center">
<img src="https://raw.githubusercontent.com/fevangelista/vmdcube/main/title.png" alt="VMDCube Header" width="450"/>
</p>

VMDCube is designed to work with VMD (Visual Molecular Dynamics) and is compatible with the VMD `cube` file format. It can be used to visualize molecular orbitals, electron density, and other volumetric data.

## Features

VMDCube can be used in Python scripts and Jupyter notebooks to render cube files. Here is an example of how to use it in Python:

```python
from vmdcube import VMDCube
vmd = VMDCube() # by default render all cube files in the current directory
vmd.run()
```

The following showcases VMDCube's visualization capabilities in Jupyter notebooks:

<p align="center">
<img src="https://raw.githubusercontent.com/fevangelista/vmdcube/main/images/example.png" alt="Example Visualization" width="450"/>
</p>

## Installation

Clone the repository, then run:

```bash
git clone git@github.com:fevangelista/VMDCube.git
cd VMDCube
pip install -e .
```

## Tutorials

See [the VMDCube introductory tutorial](tutorials/vmdcube_tutorial.ipynb) for how to use VMDCube in Jupyter notebooks.
