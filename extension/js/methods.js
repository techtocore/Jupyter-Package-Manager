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
        var html = $('<p> The following packages are about to be updated: </p> </br>');
        $('#updatebtn').toggleClass('fa-wrench fa-spinner').addClass('fa-spin');
        api.check_update(project, function (resp) {
            $('#updatebtn').toggleClass('fa-wrench fa-spinner').removeClass('fa-spin');
            var updates = resp.updates;
            var packages = [];

            if (selectedPackages.length > 0) {
                html.append($('<ul/>'));

                for (var i = 0; i < selectedPackages.length; i++) {
                    var element = selectedPackages[i];
                    element = element.split('=');
                    var pkg = element[0];
                    var ver = element[1];
                    var nver = check_new_version(updates, pkg, ver);
                    if (nver != ver) {
                        packages.push(pkg);
                        html.append("<li>" + pkg + " &nbsp; " + ver + " -> " + nver + "</li>");
                    }
                }
            }
            else {
                var list = $('.installed-values');
                html.append($('<ul/>'));
                for (var i = 0; i < list.length; i++) {
                    var element = list[i];
                    var pkg = $(element).find('.value-name')[0].innerText;
                    var ver = $(element).find('.value-version')[0].innerText;
                    var nver = check_new_version(updates, pkg, ver);
                    if (nver != ver) {
                        packages.push(pkg);
                        html.append("<li>" + pkg + " &nbsp; " + ver + " -> " + nver + "</li>");
                    }
                }
            }
            if (packages.length === 0) {
                html = $("<p> There are no updates available </p>");
                common.display_msg("Update Packages", html);
            }
            else
                common.confirm("Update Packages", html, "Confirm", function () {
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
        var html = $("<p> The following packages are about to be deleted: </p> </br>");
        html.append($('<ul/>'));
        var packages = [];
        for (var i = 0; i < selectedPackages.length; i++) {
            var element = selectedPackages[i];
            element = element.split('=')[0];
            packages.push(element);
            html.append("<li>" + element + "</li>");
        }
        common.confirm("Delete Packages", html, "Confirm", function () {
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
        var html = $("<p> The following packages are about to be added: </p> </br>");
        html.append($('<ul/>'));
        for (var i = 0; i < toInstall.length; i++) {
            var element = toInstall[i];
            element = element.split('=')[0];
            html.append("<li>" + element + "</li>");
        }
        common.confirm("Install Packages", html, "Confirm", function () {
            api.install_packages(toInstall, project);
        });
    });
}

export default {
    update_packages: update_packages,
    delete_packages: delete_packages,
    install_packages: install_packages
}