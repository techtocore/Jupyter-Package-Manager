define([
    'jquery',
    './urls',
    './api_endpoints'
], function ($, urls, endpoints) {
    "use strict";

    let ajax = {

        updatep: function (packages, project) {
            let payload = {};
            payload['project'] = project;
            payload['packages'] = packages;
            let settings = {
                "async": true,
                "crossDomain": true,
                "url": urls.api_url + endpoints.updatep.uri,
                "method": endpoints.updatep.method,
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
                "url": urls.api_url + endpoints.checkupdate.uri + project,
                "method": endpoints.checkupdate.method,
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
                "url": urls.api_url + endpoints.deletep.uri,
                "method": endpoints.deletep.method,
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
                "url": urls.api_url + endpoints.installp.uri,
                "method": endpoints.installp.method,
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

        getinfo: function (dir) {
            let settings = {
                "async": true,
                "crossDomain": true,
                "url": urls.api_url + endpoints.getinfo.uri + dir,
                "method": endpoints.getinfo.method,
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
                "url": urls.api_url + endpoints.search.uri + query,
                "method": endpoints.search.method,
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
