
# Package-Manager-API

This file outlines the API specifications for the endpoints used by Jupyter Package Manager

## Indices

* [Maintenance Tasks](#maintenance-tasks)

  * [List Projects](#1-list-projects)
  * [Delete Project List](#2-delete-project-list)

* [Package Management](#package-management)

  * [Install Packages](#1-install-packages)
  * [Uninstall Packages](#2-uninstall-packages)
  * [Check Updates for Packages](#3-check-updates-for-packages)
  * [Update Packages](#4-update-packages)
  * [Search Packages](#5-search-packages)

* [Project Management](#project-management)

  * [Create Project](#1-create-project)
  * [Delete Project](#2-delete-project)
  * [Project Info](#3-project-info)


--------


## Maintenance Tasks



### 1. List Projects


This API endpoint lists down all the projects created with this extension.


***Endpoint:***

```bash
Method: GET
Type: RAW
URL: http://localhost:8888/api/packagemanager/projects
```



### 2. Delete Project List


This API endpoint lets you delete multiple projects at once.


***Endpoint:***

```bash
Method: DELETE
Type: RAW
URL: http://localhost:8888/api/packagemanager/projects
```


***Headers:***

| Key | Value | Description |
| --- | ------|-------------|
| Content-Type | application/json |  |



***Body:***

```js        
{
	"dir": ["/home/akash/.conda/envs/swantest1", "/home/akash/.conda/envs/swantest2"]
}
```



## Package Management



### 1. Install Packages


The extension installs the package onto the corresponding project.

The .swanproject gets updated with the new package and respective version.


***Endpoint:***

```bash
Method: POST
Type: RAW
URL: http://localhost:8888/api/packagemanager/packages
```


***Headers:***

| Key | Value | Description |
| --- | ------|-------------|
| Content-Type | application/json |  |



***Body:***

```js        
{
	"dir": "/home/akash/.conda/envs/swantest",
	"packages": ["numpy"]
}
```



### 2. Uninstall Packages


The extension removes the package from the corresponding project.

The .swanproject gets updated with the current set of packages and respective versions.



***Endpoint:***

```bash
Method: DELETE
Type: RAW
URL: http://localhost:8888/api/packagemanager/packages
```


***Headers:***

| Key | Value | Description |
| --- | ------|-------------|
| Content-Type | application/json |  |



***Body:***

```js        
{
	"dir": "/home/akash/.conda/envs/swantest",
	"packages": ["numpy"]
}
```



### 3. Check Updates for Packages


This API endpoint returns the list of packages that can be updated in the corresponding project.


***Endpoint:***

```bash
Method: GET
Type: RAW
URL: http://localhost:8888/api/packagemanager/packages/check_update
```


***Headers:***

| Key | Value | Description |
| --- | ------|-------------|
| Content-Type | application/json |  |



***Query params:***

| Key | Value | Description |
| --- | ------|-------------|
| dir | /home/akash/.conda/envs/swantest |  |



### 4. Update Packages


The API endpoint installs the latest versions of packages onto the corresponding project.

The .swanproject gets updated with the new packages and respective versions.


***Endpoint:***

```bash
Method: PATCH
Type: RAW
URL: http://localhost:8888/api/packagemanager/packages
```


***Headers:***

| Key | Value | Description |
| --- | ------|-------------|
| Content-Type | application/json |  |



***Body:***

```js        
{
	"dir": "/home/akash/.conda/envs/swantest",
	"packages": ["numpy"]
}
```



### 5. Search Packages


This API endpoint lets you search a package name for installation.


***Endpoint:***

```bash
Method: GET
Type: RAW
URL: http://localhost:8888/api/packagemanager/packages/search
```



***Query params:***

| Key | Value | Description |
| --- | ------|-------------|
| q | numpy |  |



## Project Management



### 1. Create Project


The API endpoint creates a conda environment with a Python kernel installed (ipykernel).

The .swanproject file gets filled with the swanproject-UUID (name of the environment internally) and the installed packages.

A 'kernel.json' file is generated and stored, to allow the users to create a notebook from the newly created environment corresponding to the project.


***Endpoint:***

```bash
Method: POST
Type: RAW
URL: http://localhost:8888/api/packagemanager/projects
```


***Headers:***

| Key | Value | Description |
| --- | ------|-------------|
| Content-Type | application/json |  |



***Body:***

```js        
{
	"dir": "/home/akash/.conda/envs/swantest",
	"env_type": "python3"
}
```



### 2. Delete Project


The API endpoint deletes the conda environment corresponding to a project.

The 'kernel.json' for the environment corresponding to the project is removed.

Note that the project directory has to exist while calling this endpoint, and it is left unmodified by invoking this API.


***Endpoint:***

```bash
Method: DELETE
Type: RAW
URL: http://localhost:8888/api/packagemanager/projects
```


***Headers:***

| Key | Value | Description |
| --- | ------|-------------|
| Content-Type | application/json |  |



***Body:***

```js        
{
	"dir": "/home/akash/.conda/envs/swantest"
}
```



### 3. Project Info


The API endpoint outlines the details of the conda environment corresponding to a project.



***Endpoint:***

```bash
Method: GET
Type: RAW
URL: http://localhost:8888/api/packagemanager/project_info
```



***Query params:***

| Key | Value | Description |
| --- | ------|-------------|
| dir | /home/akash/.conda/envs/swantest |  |



---
[Back to top](#package-manager-api)
