define([
    'jquery',
    './urls',
    './api_endpoints'
], function ($, urls, endpoints) {
    "use strict";

    /*
    This function updates all the selected packages.
    */

    function updatep(packages, project) {
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
    }

    /*
    This function checks for updates in the selected project.
    */

    function checkupdate(project) {
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
    }

    /*
    This function removes all the selected packages.
    */

    function deletep(packages, project) {
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
    }

    function installp(packages, project) {
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
    }

    /*
    This function returns the status of all the packages in a project.
    */

    function getinfo(dir) {
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
    }

    /*
    This function lets users search using any input query.
    */

    function search(query) {
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

    return {
        'updatep': updatep,
        'installp': installp,
        'deletep': deletep,
        'getinfo': getinfo,
        'search': search,
        'checkupdate': checkupdate
    };
});
