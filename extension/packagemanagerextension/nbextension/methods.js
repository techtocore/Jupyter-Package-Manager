
define([
    'jquery',
    './common',
], function ($, common) {
    "use strict";

    var updatepkg = {

        update: function (packages, project) {
            let payload = {};
            payload['project'] = project;
            payload['packages'] = packages;
            let settings = {
                "async": true,
                "crossDomain": true,
                "url": "http://localhost:8888/api/packagemanager/packages",
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
            var settings = {
                "async": true,
                "crossDomain": true,
                "url": "http://localhost:8888/api/packagemanager/packages/check_update?project=" + project,
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

        checknewversion: function (updates, packagename, pkgversion) {
            updates.forEach(element => {
                console.log(element);
                if (element.name === packagename) {
                    return element.version;
                }
            });
            return pkgversion;
        },

        load: async function () {
            let update = this.update;
            let checkupdate = this.checkupdate;
            let checknewversion = this.checknewversion;
            jQuery(async function () {
                $('#updatebtn').click(async function () {
                    let selectedPackages = sessionStorage.getItem("selectedPackages");
                    if (null === selectedPackages)
                        selectedPackages = [];
                    else {
                        selectedPackages = selectedPackages.split(',');
                        if (selectedPackages[0].length < 1) selectedPackages = [];
                    }
                    let project = sessionStorage.getItem("project");
                    let html = "<p> The following packages are about to be updated: </p> </br>";
                    let resp = await checkupdate(project);
                    let updates = resp.updates;
                    let packages = [];
                    if (selectedPackages.length > 0) {
                        html += "<ul>";
                        selectedPackages.forEach(element => {
                            element = element.split('=');
                            packages.push(element[0]);
                            html += "<li>";
                            html += element[0] + "  ";
                            html += element[1] + " -> ";
                            html += checknewversion(updates, element[0], element[1]);
                            html += "</li>";
                        });
                        html += "</ul>";
                    }
                    else {
                        html += "<br>";
                    }
                    common.confirm("Update Packages", $.parseHTML(html), "Confirm", update(packages, project), undefined);
                });
            });
        }
    };

    var deletepkg = {

        deletep: function (packages, project) {
            let payload = {};
            payload['project'] = project;
            payload['packages'] = packages;
            let settings = {
                "async": true,
                "crossDomain": true,
                "url": "http://localhost:8888/api/packagemanager/packages",
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

        load: function () {
            let deletep = this.deletep;
            jQuery(function () {
                $('#deletebtn').click(function () {
                    let selectedPackages = sessionStorage.getItem("selectedPackages").split(',');
                    let project = sessionStorage.getItem("project");
                    // let resp = await update(selectedPackages, project);
                    let html = "<p> The following packages are about to be deleted: </p> </br>";
                    html += "<ul>";
                    let packages = [];
                    selectedPackages.forEach(element => {
                        element = element.split('=')[0];
                        packages.push(element);
                        html += "<li>";
                        html += element;
                        html += "</li>";
                    });
                    html += "</ul>";
                    common.confirm("Delete Packages", $.parseHTML(html), "Confirm", deletep(packages, project), undefined);
                });
            });
        }
    };

    var installpkg = {

        installp: function (packages, project) {
            let payload = {};
            payload['project'] = project;
            payload['packages'] = packages;
            let settings = {
                "async": true,
                "crossDomain": true,
                "url": "http://localhost:8888/api/packagemanager/packages",
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

        load: function () {
            let installp = this.installp;
            jQuery(function () {
                $('#installbtn').click(function () {
                    let toInstall = sessionStorage.getItem("toInstall").split(',');
                    let project = sessionStorage.getItem("project");
                    let html = "<p> The following packages are about to be added: </p> </br>";
                    html += "<ul>";
                    let packages = [];
                    toInstall.forEach(element => {
                        element = element.split('=')[0];
                        packages.push(element);
                        html += "<li>";
                        html += element;
                        html += "</li>";
                    });
                    html += "</ul>";
                    common.confirm("Install Packages", $.parseHTML(html), "Confirm", installp(packages, project), undefined);
                });
            });
        }
    };

    return {
        'updatepkg': updatepkg,
        'deletepkg': deletepkg,
        'installpkg': installpkg
    };
});
