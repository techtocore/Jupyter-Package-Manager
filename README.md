# Package manager for SWAN and Jupyter Notebooks 

[![Build Status](https://travis-ci.org/techtocore/Jupyter-Package-Manager.svg?branch=swan-integration)](https://travis-ci.org/techtocore/Jupyter-Package-Manager) [![Build status](https://ci.appveyor.com/api/projects/status/wo9msinix7vtotn3?svg=true)](https://ci.appveyor.com/project/techtocore/jupyter-package-manager) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=techtocore_Jupyter-Package-Manager&metric=alert_status)](https://sonarcloud.io/dashboard?id=techtocore_Jupyter-Package-Manager)


This Jupyter notebook extension will allow the users to specify python modules (and their respective versions) via a user interface and make them available automatically inside the corresponding project.

Each project is internally mapped to a separate conda environment. This helps abstract the processing part, while providing an independent environment for each project. 

## Features

- View packages installed for a specific project
- Update / Delete existing packages
- Search for new packages and install them
- Sync your project if any of your packages are missing or misconfigured

## Instructions

- This project assumes a [SWAN](https://gitlab.cern.ch/swan) setup. The APIs require certain actions as prerequisites, which are already fulfilled by SWAN. 
- Please find the install instructions [here](extension/install.md)


## Documentation

- Please find the API Specification [here](docs/API_docs.md)


## Screenshot

![Alt text](/docs/ui.png?raw=true "Package Management UI")


## About

This extension is made for the purpose of fulfilment of the GSoC 2019 project at CERN ([Project Summary](https://summerofcode.withgoogle.com/projects/4999527885438976))

- Developer: Akash Ravi
- Email ID: akashkravi@gmail.com
- Linkedin Profile: https://www.linkedin.com/in/akash-ravi/
