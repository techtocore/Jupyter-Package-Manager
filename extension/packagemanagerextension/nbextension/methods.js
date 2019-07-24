
define([
    'jquery',
    './common',
    './api',
], function ($, common, api) {
    "use strict";


    /*
    This function returns the latest version of a package.
    */

    function checknewversion(updates, packagename, pkgversion) {
        for (let element of updates) {
            if (element.name === packagename) {
                return element.version;
            }
        }
        return pkgversion;
    }

    /*
    This function lists down all the updates and requires a user confirmation.
    */

    async function updatepkg() {
        $('#updatebtn').unbind();
        $('#updatebtn').click(async function () {
            let selectedPackages = common.get_selected_packages();
            let url = location.href.split('/');
            let project = 'SWAN_projects/' + url[url.length - 1];
            let html = "<p> The following packages are about to be updated: </p> </br>";
            $('#updatebtn').toggleClass('fa-wrench fa-spinner').addClass('fa-spin');
            let resp = await api.checkupdate(project);
            $('#updatebtn').toggleClass('fa-wrench fa-spinner').removeClass('fa-spin');
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
                        html += pkg + "    " + ver + " -> " + nver;
                        html += "</li>";
                        ct += 1;
                    }
                });
                html += "</ul>";
            }
            else {
                let list = $('.installed-values');
                html += "<ul>";
                for (let item of list) {
                    let pkg = $(item).find('.value-name')[0].innerText;
                    let ver = $(item).find('.value-version')[0].innerText;
                    let nver = checknewversion(updates, pkg, ver);
                    if (nver != ver) {
                        packages.push(pkg);
                        html += "<li>";
                        html += pkg + "    " + ver + " -> " + nver;
                        html += "</li>";
                        ct += 1;
                    }
                }
                html += "</ul>";
            }
            if (ct === 0) {
                html = "<p> There are no updates available </p>"
            }
            common.confirm("Update Packages", $.parseHTML(html), "Confirm", function () {
                api.update_packages(packages, project);
            });
        });
    }


    /*
    This function lists down all the packages selected for removal and requires a user confirmation.
    */

    function deletepkg() {
        $('#deletebtn').unbind();
        $('#deletebtn').click(function () {
            let selectedPackages = common.get_selected_packages();
            let url = location.href.split('/');
            let project = 'SWAN_projects/' + url[url.length - 1];
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
            if (packages.length === 0)
                html = "<p> No packages selected </p>";
            common.confirm("Delete Packages", $.parseHTML(html), "Confirm", function () {
                api.delete_packages(packages, project);
            });
        });
    }


    /*
    This function lists down all the packages selected for installation and requires a user confirmation.
    */

    function installpkg() {
        $('#installbtn').unbind();
        $('#installbtn').click(function () {
            let toInstall = common.get_to_install();
            let project = 'SWAN_projects/' + location.href.split('/')[this.length];
            let html = "<p> The following packages are about to be added: </p> </br>";
            html += "<ul>";
            toInstall.forEach(element => {
                element = element.split('=')[0];
                html += "<li>";
                html += element;
                html += "</li>";
            });
            html += "</ul>";
            if (toInstall.length === 0)
                html = "<p> No packages selected </p>";
            common.confirm("Install Packages", $.parseHTML(html), "Confirm", function () {
                api.install_packages(toInstall, project);
            });
        });
    }

    return {
        'updatepkg': updatepkg,
        'deletepkg': deletepkg,
        'installpkg': installpkg
    };
});
