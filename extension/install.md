# Installation

## Docker Setup

This lets you try out this extension on a local containerized setup of SWAN. This includes a preview of the integration with SWAN contents.

- Create a container from the Dockerfile
```bash
docker build . -t swanimage
docker create -t --name swancontainer -p 8888:8888 swanimage
```

- Start or stop the container
```bash
docker start swancontainer
docker stop swancontainer
```

- The logs of the container can be checked using 
```bash 
docker logs swancontainer 
```

- The root shell of the container can be accessed using
```bash 
docker exec -u root -it swancontainer /bin/bash
```

- By default, the application will run on port 8888

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