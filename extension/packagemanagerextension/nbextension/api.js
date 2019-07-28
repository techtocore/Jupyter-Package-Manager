define([
    'jquery',
    './urls',
    './common'
], function ($, urls, common) {
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

    function api_call(endpoint, url, payload = {}) {

        let settings = {
            "url": urls.api_url + endpoint.uri + url,
            "method": endpoint.method,
            "headers": {
                "Content-Type": "application/json",
                "cache-control": "no-cache",
            },
            "processData": false
        };

        // Send the payload only if it is not empty

        if (!(Object.keys(payload).length === 0 && payload.constructor === Object)) {
            settings.data = JSON.stringify(payload);
        }

        return new Promise(resolve => {
            $.ajax(settings).done(function (response) {
                resolve(response);
            }).fail(function () {
                common.display_msg("Server Error", "Please Try again");
            });
        });
    }

    /*
    This function updates all the selected packages.
    */

    function update_packages(packages, project) {
        let payload = {
            'project': project,
            'packages': packages
        };
        return api_call(endpoints.update_packages, "", payload);
    }

    /*
    This function checks for updates in the selected project.
    */

    function check_update(project) {
        return api_call(endpoints.checkupdate, project);
    }

    /*
    This function removes all the selected packages.
    */

    function delete_packages(packages, project) {
        let payload = {
            'project': project,
            'packages': packages
        };
        return api_call(endpoints.delete_packages, "", payload);
    }

    function install_packages(packages, project) {
        let payload = {
            'project': project,
            'packages': packages
        };
        return api_call(endpoints.install_packages, "", payload);
    }

    /*
    This function returns the status of all the packages in a project.
    */

    function get_info(dir) {
        return api_call(endpoints.getinfo, dir);
    }

    /*
    This function lets users search using any input query.
    */

    function search(query) {
        return api_call(endpoints.search, query);
    }

    return {
        update_packages,
        install_packages,
        delete_packages,
        get_info,
        search,
        check_update
    };
});
