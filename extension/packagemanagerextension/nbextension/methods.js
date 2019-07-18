
define([
    'jquery',
    './common',
    './api',
], function ($, common, api) {
    "use strict";

    let updatepkg = {

        checknewversion: function (updates, packagename, pkgversion) {
            for (let element of updates) {
                if (element.name === packagename) {
                    return element.version;
                }
            }
            return pkgversion;
        },

        load: async function () {
            let updatep = api.ajax.updatep;
            let checkupdate = api.ajax.checkupdate;
            let checknewversion = this.checknewversion;
            $(async function () {
                $('#updatebtn').unbind();
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
                    let ct = 0;
                    if (selectedPackages.length > 0) {
                        html += "<ul>";
                        selectedPackages.forEach(element => {
                            element = element.split('=');
                            let pkg = element[0];
                            let ver = element[1];
                            let nver = checknewversion(updates, pkg, ver);
                            if (nver != ver) {
                                packages.push(pkg);
                                html += "<li>";
                                html += pkg + "  ";
                                html += ver + " -> ";
                                html += nver;
                                html += "</li>";
                                ct += 1;
                            }
                        });
                        html += "</ul>";
                    }
                    else {
                        let list = document.getElementsByClassName("installed-values");
                        html += "<ul>";
                        for (let item of list) {
                            let pkg = item.getElementsByClassName('value-name')[0].innerText;
                            let ver = item.getElementsByClassName('value-version')[0].innerText;
                            let nver = checknewversion(updates, pkg, ver);
                            if (nver != ver) {
                                packages.push(pkg);
                                html += "<li>";
                                html += pkg + "  ";
                                html += ver + " -> ";
                                html += nver;
                                html += "</li>";
                                ct += 1;
                            };
                        }
                        html += "</ul>";
                    }
                    if (ct === 0) {
                        html = "<p> There are no updates available </p>"
                    }
                    common.confirm("Update Packages", $.parseHTML(html), "Confirm", function () {
                        updatep(packages, project);
                    });
                });
            });
        }
    };

    let deletepkg = {

        load: function () {
            let deletep = api.ajax.deletep;
            $(function () {
                $('#deletebtn').unbind();
                $('#deletebtn').click(function () {
                    let selectedPackages = sessionStorage.getItem("selectedPackages").split(',');
                    let project = sessionStorage.getItem("project");
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
                    common.confirm("Delete Packages", $.parseHTML(html), "Confirm", function () {
                        deletep(packages, project);
                    });
                });
            });
        }
    };

    let installpkg = {

        load: function () {
            let installp = api.ajax.installp;
            $(function () {
                $('#installbtn').unbind();
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
                    common.confirm("Install Packages", $.parseHTML(html), "Confirm", function () {
                        installp(packages, project);
                    });
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
