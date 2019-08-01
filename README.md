# Package manager for SWAN and Jupyter Notebooks 

[![Build status](https://ci.appveyor.com/api/projects/status/wo9msinix7vtotn3/branch/dev?svg=true)](https://ci.appveyor.com/project/techtocore/jupyter-package-manager/branch/dev)


This Jupyter notebook extension will allow the users to specify python modules (and their respective versions) via a user interface and make them available automatically inside the corresponding project.

Each project is internally mapped to a separate conda environment. This helps abstract the processing part, while providing an independent environment for each project. 

## Instructions

- This project assumes a [SWAN](https://gitlab.cern.ch/swan) setup. The APIs require certain actions as prerequisites, which are already fulfilled by SWAN. 
- Please find the install instructions [here](extension/install.md)
- For the purpose of API testing and development, please allow cross-site requests by adding `c.NotebookApp.disable_check_xsrf = True` (in ~/.jupyter/jupyter_notebook_config.py)


## Documentation

- Please find the API Specification [here](docs/API_docs.md)


## Screenshot

![Alt text](/docs/ui.png?raw=true "Package Management UI")


## About

This extension is made for the purpose of fulfilment of the GSoC 2019 project at CERN ([Read Proposal Here](https://summerofcode.withgoogle.com/projects/4999527885438976))

- Developer: Akash Ravi
- Email ID: akashkravi@gmail.com
