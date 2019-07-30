
define([
    'jquery',
    './common',
    './api',
], function ($, common, api) {
    "use strict";

    /*
    This function returns the latest version of a package.
    */

    function check_new_version(updates, packagename, pkgversion) {
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

    function update_packages(project) {
        $('#updatebtn').unbind();
        $('#updatebtn').click(function () {
            let selectedPackages = common.get_selected_packages();
            let html = "<p> The following packages are about to be updated: </p> </br>";
            $('#updatebtn').toggleClass('fa-wrench fa-spinner').addClass('fa-spin');
            api.check_update(project, function (resp) {
                $('#updatebtn').toggleClass('fa-wrench fa-spinner').removeClass('fa-spin');
                let updates = resp.updates;
                let packages = [];
                let ct = 0;

                if (selectedPackages.length > 0) {
                    html += "<ul>";
                    for (let element of selectedPackages) {
                        element = element.split('=');
                        let pkg = element[0];
                        let ver = element[1];
                        let nver = check_new_version(updates, pkg, ver);
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
                else {
                    let list = $('.installed-values');
                    html += "<ul>";
                    for (let item of list) {
                        let pkg = $(item).find('.value-name')[0].innerText;
                        let ver = $(item).find('.value-version')[0].innerText;
                        let nver = check_new_version(updates, pkg, ver);
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
                    common.dispay_msg("Install Packages", $.parseHTML(html));
                }
                else
                    common.confirm("Update Packages", $.parseHTML(html), "Confirm", function () {
                        api.update_packages(packages, project);
                    });
            });

        });
    }


    /*
    This function lists down all the packages selected for removal and requires a user confirmation.
    */

    function delete_packages(project) {
        $('#deletebtn').unbind();
        $('#deletebtn').click(function () {
            let selectedPackages = common.get_selected_packages();
            let html = "<p> The following packages are about to be deleted: </p> </br>";
            html += "<ul>";
            let packages = [];
            for (let element of selectedPackages) {
                element = element.split('=')[0];
                packages.push(element);
                html += "<li>";
                html += element;
                html += "</li>";
            }
            html += "</ul>";
            if (packages.length === 0) {
                html = "<p> No packages selected </p>";
                common.dispay_msg("Install Packages", $.parseHTML(html));
            }
            else
                common.confirm("Delete Packages", $.parseHTML(html), "Confirm", function () {
                    api.delete_packages(packages, project);
                });
        });
    }


    /*
    This function lists down all the packages selected for installation and requires a user confirmation.
    */

    function install_packages(project) {
        $('#installbtn').unbind();
        $('#installbtn').click(function () {
            let toInstall = common.get_to_install();
            let html = "<p> The following packages are about to be added: </p> </br>";
            html += "<ul>";
            for (let element of toInstall) {
                element = element.split('=')[0];
                html += "<li>";
                html += element;
                html += "</li>";
            }
            html += "</ul>";
            if (toInstall.length === 0) {
                html = "<p> No packages selected </p>";
                common.dispay_msg("Install Packages", $.parseHTML(html));
            }
            else
                common.confirm("Install Packages", $.parseHTML(html), "Confirm", function () {
                    api.install_packages(toInstall, project);
                });
        });
    }

    return {
        update_packages,
        delete_packages,
        install_packages
    };
});
