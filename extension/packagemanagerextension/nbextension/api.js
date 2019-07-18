define([
    'jquery',
    './urls',
], function ($, urls) {
    "use strict";

    let ajax = {

        update: function (packages, project) {
            let payload = {};
            payload['project'] = project;
            payload['packages'] = packages;
            let settings = {
                "async": true,
                "crossDomain": true,
                "url": urls.api_url + "packages",
                "method": "PATCH",
                "headers": {
                    "Content-Type": "application/json",
                    "cache-control": "no-cache",
                },
                "processData": false,
                "data": JSON.stringify(payload)
            };


            return new Promise(resolve => {
                $.ajax(settings).done(function (response) {
                    resolve(response);
                });
            });
        },

        checkupdate: function (project) {
            let settings = {
                "async": true,
                "crossDomain": true,
                "url": urls.api_url + "packages/check_update?project=" + project,
                "method": "GET",
                "headers": {
                    "Content-Type": "application/json",
                    "cache-control": "no-cache"
                },
                "processData": false,
                "data": ""
            };

            return new Promise(resolve => {
                $.ajax(settings).done(function (response) {
                    resolve(response);
                });
            });
        },

        deletep: function (packages, project) {
            let payload = {};
            payload['project'] = project;
            payload['packages'] = packages;
            let settings = {
                "async": true,
                "crossDomain": true,
                "url": urls.api_url + "packages",
                "method": "DELETE",
                "headers": {
                    "Content-Type": "application/json",
                    "cache-control": "no-cache",
                },
                "processData": false,
                "data": JSON.stringify(payload)
            };


            return new Promise(resolve => {
                $.ajax(settings).done(function (response) {
                    resolve(response);
                });
            });
        },

        installp: function (packages, project) {
            let payload = {};
            payload['project'] = project;
            payload['packages'] = packages;
            let settings = {
                "async": true,
                "crossDomain": true,
                "url": urls.api_url + "packages",
                "method": "POST",
                "headers": {
                    "Content-Type": "application/json",
                    "cache-control": "no-cache",
                },
                "processData": false,
                "data": JSON.stringify(payload)
            };


            return new Promise(resolve => {
                $.ajax(settings).done(function (response) {
                    resolve(response);
                });
            });
        },

        get_info: function (dir) {
            let settings = {
                "async": true,
                "crossDomain": true,
                "url": urls.api_url + "project_info?project=" + dir,
                "method": "GET",
                "headers": {
                    "Content-Type": "application/json",
                    "cache-control": "no-cache",
                },
                "processData": false,
                "data": ""
            };

            return new Promise(resolve => {
                $.ajax(settings).done(function (response) {
                    resolve(response);
                });
            });
        },

        search: function (query) {
            let settings = {
                "async": true,
                "crossDomain": true,
                "url": urls.api_url + "packages/search?q=" + query,
                "method": "GET",
                "headers": {
                    "cache-control": "no-cache"
                }
            };

            return new Promise(resolve => {
                $.ajax(settings).done(function (response) {
                    resolve(response);
                });
            });
        }

    };

    return {
        'ajax': ajax
    };
});
