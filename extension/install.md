# Installation

## Docker Setup

This lets you try out this extension on a local containerized setup of SWAN. This includes a preview of the integration with SWAN contents. 

*TODO: Add instructions*

## Development Setup
- Prerequisites
    - [Git](https://git-scm.com/)
    - [Python 3](https://www.python.org/downloads/)
    - [Jupyter Notebook](http://jupyter.org/)
    - [Yarn](https://yarnpkg.com/lang/en/docs/install)


- Download extension
```
git clone https://github.com/techtocore/Jupyter-Package-Manager.git
cd Jupyter-Package-Manager/extension
```

- Build and Install Dependencies
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

- For the purpose of API testing and development, please allow cross-site requests by adding c.NotebookApp.disable_check_xsrf = True (in ~/.jupyter/jupyter_notebook_config.py)