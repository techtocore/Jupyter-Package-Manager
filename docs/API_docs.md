
# Package-Manager-API

This file outlines the API specifications for the endpoints used by Jupyter Package Manager

## Indices

* [Project Management](#project-management)

  * [Create Project](#1-create-project)
  * [Delete Project](#2-delete-project)
  * [Project Export](#3-project-export)
  * [Project Info](#4-project-info)
  * [Project Import](#5-project-import)
  * [Sync Project](#6-sync-project)
  * [Clone Project](#7-clone-project)

* [Package Management](#package-management)

  * [Install Packages](#1-install-packages)
  * [Uninstall Packages](#2-uninstall-packages)
  * [Check Updates for Packages](#3-check-updates-for-packages)
  * [Update Packages](#4-update-packages)
  * [Search Packages](#5-search-packages)

* [Maintenance Tasks](#maintenance-tasks)

  * [List Projects](#1-list-projects)
  * [Delete Project List](#2-delete-project-list)

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


***Sample Output:***

```js
{
    "projects": [
        {
            "name": "swanproject-ad4d7f04-98c6-11e9-830c-ac2b6ebe8a16",
            "dir": "/home/akash/.conda/envs/swanproject-ad4d7f04-98c6-11e9-830c-ac2b6ebe8a16"
        }
    ]
}
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
	"project": ["/MySwanProjectA", "/MySwanProjectB"]
}
```

***Sample Output:***

```js
{
    "response":
    [
        {
	    "prefix": "/home/akash/.conda/envs/swanproject-ad4d7f04-98c6-11e9-830c-ac2b6ebe8a16",
	    "success": true,
	    "actions": {
		"PREFIX": "/home/akash/.conda/envs/swanproject-ad4d7f04-98c6-11e9-830c-ac2b6ebe8a16",
		"UNLINK": [
		    {
			"dist_name": "ipython_genutils-0.2.0-py37_0",
			"build_number": 0,
			"name": "ipython_genutils",
			"build_string": "py37_0",
			"base_url": "https://repo.anaconda.com/pkgs/main",
			"platform": "linux-64",
			"version": "0.2.0",
			"channel": "pkgs/main"
		    }
		],
		"FETCH": []
	    }
	}
    ]
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
	"project": "/MySwanProjectA",
	"packages": ["pyyaml=3.13"]
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
	"project": "/MySwanProjectA",
	"packages": ["pyyaml"]
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
| project | /MySwanProjectA |  |



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
	"project": "/MySwanProjectA",
	"packages": ["pyyaml"]
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
| q | pyyaml=3.13 |  |



## Project Management



### 1. Create Project


The API endpoint creates a conda environment with a Python kernel installed (ipykernel).

The .swanproject file gets filled with the swanproject-UUID (name of the environment internally) and the installed packages.



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
	"project": "/MySwanProjectA",
	"env_type": "python3"
}
```

***Sample Output:***

```js
{
    "prefix": "/home/akash/.conda/envs/swanproject-ad4d7f04-98c6-11e9-830c-ac2b6ebe8a16",
    "success": true,
    "actions": {
        "PREFIX": "/home/akash/.conda/envs/swanproject-ad4d7f04-98c6-11e9-830c-ac2b6ebe8a16",
        "LINK": [
            {
                "dist_name": "ipython_genutils-0.2.0-py37_0",
                "build_number": 0,
                "name": "ipython_genutils",
                "build_string": "py37_0",
                "base_url": "https://repo.anaconda.com/pkgs/main",
                "platform": "linux-64",
                "version": "0.2.0",
                "channel": "pkgs/main"
            }
        ],
        "FETCH": []
    }
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
	"project": ["/MySwanProjectA"]
}
```



### 3. Project Export


The API endpoint exports the details of the conda environment corresponding to a project.



***Endpoint:***

```bash
Method: GET
Type: RAW
URL: http://localhost:8888/api/packagemanager/project_info
```


***Headers:***

| Key | Value | Description |
| --- | ------|-------------|
| Content-Type | text/plain |  |



***Query params:***

| Key | Value | Description |
| --- | ------|-------------|
| project | /MySwanProjectA |  |

***Sample Output:***

```
# This file may be used to create an environment using:
# $ conda create --name <env> --file <this file>
# platform: linux-64
_libgcc_mutex=0.1=main
backcall=0.1.0=py37_0
blas=1.0=mkl
```


### 4. Project Info


The API endpoint outlines the details of the conda environment corresponding to a project.



***Endpoint:***

```bash
Method: GET
Type: RAW
URL: http://localhost:8888/api/packagemanager/project_info
```


***Headers:***

| Key | Value | Description |
| --- | ------|-------------|
| Content-Type | application/json |  |



***Query params:***

| Key | Value | Description |
| --- | ------|-------------|
| project | /MySwanProjectA |  |

***Sample Output:***

```
{
    "packages": [
        {
            "status": "installed",
            "version": "3.28.0",
            "build_string": "h7b6447c_0",
            "name": "sqlite"
        }
    ],
    "env": "swanproject-729350f4-9e8f-11e9-b575-ac2b6ebe8a16"
}
```

### 5. Project Import


This API endpoint updates a project with all the packages obtained from an export file.


***Endpoint:***

```bash
Method: PUT
Type: FORMDATA
URL: http://localhost:8888/api/packagemanager/project_info
```


***Headers:***

| Key | Value | Description |
| --- | ------|-------------|
| Content-Type | application/x-www-form-urlencoded |  |



***Body:***

| Key | Value | Description |
| --- | ------|-------------|
| file |  |  |
| project | /MySwanProjectA |  |



### 6. Sync Project


This API endpoint syncs a .swanproject file and the corresponding conda env.


***Endpoint:***

```bash
Method: PATCH
Type: RAW
URL: http://localhost:8888/api/packagemanager/project_info
```


***Headers:***

| Key | Value | Description |
| --- | ------|-------------|
| Content-Type | application/json |  |



***Body:***

```js        
{
	"project": "/MySwanProjectA"
}
```



### 7. Clone Project


This enpoint creates a new env for a folder that has just been cloned.


***Endpoint:***

```bash
Method: POST
Type: RAW
URL: http://localhost:8888/api/packagemanager/project_clone
```


***Headers:***

| Key | Value | Description |
| --- | ------|-------------|
| Content-Type | application/json |  |



***Body:***

```js        
{
	"project": "/MySwanProjectB"
}
```



---
[Back to top](#package-manager-api)
