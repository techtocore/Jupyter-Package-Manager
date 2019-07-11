# Installation

## Prerequisite
- [Jupyter Notebook](http://jupyter.org/)

## Install
Install directly from source
```
git clone https://github.com/techtocore/Jupyter-Package-Manager.git
cd Jupyter-Package-Manager/extension
python -m pip install -e .
```
- Install and enable `nbextension` in Jupyter Namespace
```bash
jupyter nbextension install --py packagemanagerextension --sys-prefix --symlink
jupyter nbextension enable packagemanagerextension --sys-prefix --py
```

- Enable Jupyter Server Extension
```bash
jupyter serverextension enable --py --sys-prefix packagemanagerextension
```
