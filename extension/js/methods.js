import $ from 'jquery';
import common from './common';
import api from './api';

/*
This function returns the latest version of a package.
*/

function check_new_version(updates, packagename, pkgversion) {
    for (var i = 0; i < updates.length; i++) {
        var element = updates[i];
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
        var selectedPackages = common.get_selected_packages();
        var html = "<p> The following packages are about to be updated: </p> </br>";
        $('#updatebtn').toggleClass('fa-wrench fa-spinner').addClass('fa-spin');
        api.check_update(project, function (resp) {
            $('#updatebtn').toggleClass('fa-wrench fa-spinner').removeClass('fa-spin');
            var updates = resp.updates;
            var packages = [];
            var ct = 0;

            if (selectedPackages.length > 0) {
                html += "<ul>";
                for (var i = 0; i < selectedPackages.length; i++) {
                    var element = selectedPackages[i];
                    element = element.split('=');
                    var pkg = element[0];
                    var ver = element[1];
                    var nver = check_new_version(updates, pkg, ver);
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
                var list = $('.installed-values');
                html += "<ul>";
                for (var i = 0; i < list.length; i++) {
                    var element = list[i];
                    var pkg = $(element).find('.value-name')[0].innerText;
                    var ver = $(element).find('.value-version')[0].innerText;
                    var nver = check_new_version(updates, pkg, ver);
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
        var selectedPackages = common.get_selected_packages();
        var html = "<p> The following packages are about to be deleted: </p> </br>";
        html += "<ul>";
        var packages = [];
        for (var i = 0; i < selectedPackages.length; i++) {
            var element = selectedPackages[i];
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
        var toInstall = common.get_to_install();
        var html = "<p> The following packages are about to be added: </p> </br>";
        html += "<ul>";
        for (var i = 0; i < toInstall.length; i++) {
            var element = toInstall[i];
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

export default {
    update_packages: update_packages,
    delete_packages: delete_packages,
    install_packages: install_packages
}