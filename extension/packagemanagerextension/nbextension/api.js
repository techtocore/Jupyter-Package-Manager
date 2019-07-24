define([
    'jquery',
    './urls'
], function ($, urls) {
    "use strict";

    let endpoints = {
        "update_packages": {
            "uri": "packages",
            "method": "PATCH"
        },
        "checkupdate": {
            "uri": "packages/check_update?project=",
            "method": "GET"
        },
        "delete_packages": {
            "uri": "packages",
            "method": "DELETE"
        },
        "install_packages": {
            "uri": "packages",
            "method": "POST"
        },
        "getinfo": {
            "uri": "project_info?project=",
            "method": "GET"
        },
        "search": {
            "uri": "packages/search?q=",
            "method": "GET"
        }
    };

    /*
    This function makes the API calls to the specified endpoint with the corresponding headers
    */
    function api_call(url, method, payload = "") {
        let settings = {
            "url": url,
            "method": method,
            "headers": {
                "Content-Type": "application/json",
                "cache-control": "no-cache",
            },
            "processData": false,
            "data": payload
        };

        return new Promise(resolve => {
            $.ajax(settings).done(function (response) {
                resolve(response);
            });
        });
    }

    /*
    This function updates all the selected packages.
    */

    function update_packages(packages, project) {
        let payload = {};
        payload['project'] = project;
        payload['packages'] = packages;
        return api_call(urls.api_url + endpoints.update_packages.uri, endpoints.update_packages.method, JSON.stringify(payload));
    }

    /*
    This function checks for updates in the selected project.
    */

    function checkupdate(project) {
        return api_call(urls.api_url + endpoints.checkupdate.uri + project, endpoints.checkupdate.method);
    }

    /*
    This function removes all the selected packages.
    */

    function delete_packages(packages, project) {
        let payload = {};
        payload['project'] = project;
        payload['packages'] = packages;
        return api_call(urls.api_url + endpoints.delete_packages.uri, endpoints.delete_packages.method, JSON.stringify(payload));
    }

    function install_packages(packages, project) {
        let payload = {};
        payload['project'] = project;
        payload['packages'] = packages;
        return api_call(urls.api_url + endpoints.install_packages.uri, endpoints.install_packages.method, JSON.stringify(payload));
    }

    /*
    This function returns the status of all the packages in a project.
    */

    function getinfo(dir) {
        return api_call(urls.api_url + endpoints.getinfo.uri + dir, endpoints.getinfo.method);
    }

    /*
    This function lets users search using any input query.
    */

    function search(query) {
        return api_call(urls.api_url + endpoints.search.uri + query, endpoints.search.method);
    }

    return {
        'update_packages': update_packages,
        'install_packages': install_packages,
        'delete_packages': delete_packages,
        'getinfo': getinfo,
        'search': search,
        'checkupdate': checkupdate
    };
});
