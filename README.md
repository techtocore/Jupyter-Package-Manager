# Package manager for SWAN and Jupyter Notebooks 

[![Build Status](https://travis-ci.org/techtocore/Jupyter-Package-Manager.svg?branch=swan-integration)](https://travis-ci.org/techtocore/Jupyter-Package-Manager) [![Build status](https://ci.appveyor.com/api/projects/status/wo9msinix7vtotn3?svg=true)](https://ci.appveyor.com/project/techtocore/jupyter-package-manager) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=techtocore_Jupyter-Package-Manager&metric=alert_status)](https://sonarcloud.io/dashboard?id=techtocore_Jupyter-Package-Manager)


**[Link to Final Report](https://akashravi.github.io/SWAN-Package-Manager/)**


This Jupyter notebook extension will allow the users to install python modules (and their respective versions) via a user interface and make them available automatically inside the corresponding project.

Each project is internally mapped to a separate conda environment. This helps abstract the processing part, while providing an independent environment for each project. 


## Features

- View packages installed for a specific project
- Update / Delete existing packages
- Search for new packages and install them
- Sync your project if any of your packages are missing or misconfigured


## Setup Instructions

- This project assumes a SWAN setup. The APIs require certain actions as prerequisites, which are already fulfilled by SWAN. 

- Please find the install instructions [here](https://github.com/techtocore/Jupyter-Package-Manager/blob/swan-integration/extension/install.md)


## Usage Instructions

- From the Projects tab, you can create a folder by clicking on the  **`+`** button. Internally, this will create a new conda environment for all the notebooks inside it.

- To configure the project, click the cog button. This would reveal a side panel listing down the installed packages, along with their corresponding versions. 

- If in case the project metadata and the underlying environment are not in sync, the sidebar will also list the packages that need to be additionally installed. This is fundamental to share projects and collaborate with peers. By default, when a user clones a shared project, the required packages are not installed. This extension will let users install them.

- To install a new package, the user can search for them (an autocomplete feature is available). The selected packages are installed only when the user clicks the 'install' button. This allows the selection of other packages before issuing the 'install' command, which might take a while.

- Users can check for updates, for all or only the selected packages, by clicking the small cog button beside the list of installed packages. A pop-up modal will list the packages that need to be updated, along with their versions. Similarly, users can select one or more packages and uninstall them by clicking the bin icon.

- In order to create a notebook, click on the **`+`** button from inside a project or a regular folder. A list will then appear with the available kernels. Users will be able to launch notebooks only using the kernel corresponding to that project. Any external notebook (requiring a python kernel) placed under the project will also be using the same kernel.


## Documentation

- Please find the API Specification [here](docs/API_docs.md)
- The code is documented with necessary inline comments and docstrings


## Screenshot

![Alt text](/docs/ui.png?raw=true "Package Management UI")


## About

This extension is made for the purpose of fulfilment of the GSoC 2019 project at CERN ([Project Summary](https://summerofcode.withgoogle.com/projects/4999527885438976))

- Developer: Akash Ravi
- Email ID: akashkravi@gmail.com
- Linkedin Profile: https://www.linkedin.com/in/akash-ravi/
