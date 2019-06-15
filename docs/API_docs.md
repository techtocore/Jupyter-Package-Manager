
# Package-Manager-API



## Indices

* [Environment Management](#environment-management)

  * [List Environments](#1-list-environments)
  * [Export Environment](#2-export-environment)
  * [Create  Environment](#3-create--environment)
  * [Clone Environment](#4-clone-environment)
  * [Delete Environment](#5-delete-environment)

* [Package Management](#package-management)

  * [List Packages](#1-list-packages)
  * [Install Packages](#2-install-packages)
  * [Uninstall Packages](#3-uninstall-packages)
  * [Check Updates for Packages](#4-check-updates-for-packages)
  * [Update Packages](#5-update-packages)
  * [Available Packages](#6-available-packages)
  * [Search Packages](#7-search-packages)


--------


## Environment Management



### 1. List Environments



***Endpoint:***

```bash
Method: GET
Type: RAW
URL: http://localhost:8888/api/packagemanager/environments
```



### 2. Export Environment



***Endpoint:***

```bash
Method: GET
Type: RAW
URL: http://localhost:8888/api/packagemanager/environment_export/myenv
```



### 3. Create  Environment



***Endpoint:***

```bash
Method: POST
Type: RAW
URL: http://localhost:8888/api/packagemanager/environment_create
```


***Headers:***

| Key | Value | Description |
| --- | ------|-------------|
| Content-Type | application/json |  |



***Body:***

```js        
{
	"env": "myenv",
	"env_type": "python3"
}
```



### 4. Clone Environment



***Endpoint:***

```bash
Method: POST
Type: RAW
URL: http://localhost:8888/api/packagemanager/environment_clone
```


***Headers:***

| Key | Value | Description |
| --- | ------|-------------|
| Content-Type | application/json |  |



***Body:***

```js        
{
	"env": "myenv",
	"new_env": "myenv1"
}
```



### 5. Delete Environment



***Endpoint:***

```bash
Method: POST
Type: RAW
URL: http://localhost:8888/api/packagemanager/environment_delete
```


***Headers:***

| Key | Value | Description |
| --- | ------|-------------|
| Content-Type | application/json |  |



***Body:***

```js        
{
	"env": "myenv"
}
```



## Package Management



### 1. List Packages



***Endpoint:***

```bash
Method: GET
Type: RAW
URL: http://localhost:8888/api/packagemanager/list_packages/myenv
```



### 2. Install Packages



***Endpoint:***

```bash
Method: POST
Type: RAW
URL: http://localhost:8888/api/packagemanager/install_packages
```


***Headers:***

| Key | Value | Description |
| --- | ------|-------------|
| Content-Type | application/json |  |



***Body:***

```js        
{
	"env": "myenv",
	"packages": ["dnspython", "pillow"]
}
```



### 3. Uninstall Packages



***Endpoint:***

```bash
Method: DELETE
Type: RAW
URL: http://localhost:8888/api/packagemanager/delete_packages
```


***Headers:***

| Key | Value | Description |
| --- | ------|-------------|
| Content-Type | application/json |  |



***Body:***

```js        
{
	"env": "myenv",
	"packages": ["sqlite"]
}
```



### 4. Check Updates for Packages



***Endpoint:***

```bash
Method: POST
Type: RAW
URL: http://localhost:8888/api/packagemanager/check_update_packages
```


***Headers:***

| Key | Value | Description |
| --- | ------|-------------|
| Content-Type | application/json |  |



***Body:***

```js        
{
	"env": "myenv",
	"packages": ["tk"]
}
```



### 5. Update Packages



***Endpoint:***

```bash
Method: PATCH
Type: RAW
URL: http://localhost:8888/api/packagemanager/update_packages
```


***Headers:***

| Key | Value | Description |
| --- | ------|-------------|
| Content-Type | application/json |  |



***Body:***

```js        
{
	"env": "myenv",
	"packages": ["tk"]
}
```



### 6. Available Packages



***Endpoint:***

```bash
Method: GET
Type: RAW
URL: http://localhost:8888/api/packagemanager/packages/available
```



### 7. Search Packages



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



---
[Back to top](#package-manager-api)
> Made with &#9829; by [thedevsaddam](https://github.com/thedevsaddam) | Generated at: 2019-06-15 15:57:05 by [docgen](https://github.com/thedevsaddam/docgen)
