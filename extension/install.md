# Installation

## Prerequisite
- [Jupyter Notebook](http://jupyter.org/)

## Install
Install directly from source
```
git clone https://github.com/techtocore/Jupyter-Package-Manager.git
cd Jupyter-Package-Manager/extension
```

- Build and Install Prerequisites
```bash
yarn install
yarn run webpack
python -m pip install -e .
```

- Install and enable `nbextension` in Jupyter Namespace
```bash
jupyter nbextension install --py packagemanager --system --symlink
jupyter nbextension enable packagemanager --system --py
```

- Enable Jupyter Server Extension
```bash
jupyter serverextension enable --py --system packagemanager
```
