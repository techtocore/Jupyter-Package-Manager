
define([
    'jquery',
    './common',
], function ($) {
    "use strict";

    /*
    This function generates the DOM for displaying packages that are selected for installation.
    */

    function toinstall(data) {
        let output = "";
        $.each(data, function (key, val) {
            if (val.status != "installed") {
                output += "<div class='to-install-values'>";
                output += "<div class='row one'>";
                output += "<div class='col-sm-9 two'>";
                output += "<i class='fa fa-check'></i> &nbsp;"
                output += '<span class="value-name">' + val.name + '</span>';
                output += "</div>";
                output += "<div class='col-sm-3 three'>";
                output += '<span class="value-version">' + val.version + '</span>'
                output += "</div>";
                output += "</div>";
                output += "</div>";
            }
        });
        return output;
    }

    /*
    This function generates the DOM for displaying packages that are currently installed.
    */

    function installed(data) {
        let output = "";
        $.each(data, function (key, val) {
            if (val.status === "installed") {
                output += "<div class='installed-values'>";
                output += "<div class='row one'>";
                output += "<div class='col-sm-9 two'>";
                output += "<i class='fa fa-cube'></i> &nbsp;"
                output += '<span class="value-name">' + val.name + '</span>';
                output += "</div>";
                output += "<div class='col-sm-3 three'>";
                output += '<span class="value-version">' + val.version + '</span>'
                output += "</div>";
                output += "</div>";
                output += "</div>";
            }

        });
        return output;
    }

    /*
    This function add an eventlistener to the DOM for handling packages that are selected for installation.
    */

    function selecttoinstall(toInstall) {
        $('.to-install-values').unbind();
        $('.to-install-values').hover(function () {
            $(this).children(".one").children(".two").find('i').toggleClass('fa-close');
        });
        $('.to-install-values').click(function () {
            let packageName = $(this).children(".one").children(".two").children(".value-name").text();
            let version = $(this).children(".one").children(".three").children(".value-version").text();
            let pkg = packageName + "=" + version;
            if (toInstall.includes(pkg)) {
                toInstall = toInstall.filter(item => item !== pkg);
                $(this).remove();
            }
            if (toInstall.length === 0) {
                $('#to-install-main').css("display", "none");
            }
        });
    }

    /*
    This function add an eventlistener to the DOM for handling packages that are currently installed.
    */

    function selectinstalled(selectedPackages) {
        $('.installed-values').unbind();
        $('.installed-values').click(function () {
            let packageName = $(this).children(".one").children(".two").children(".value-name").text();
            let version = $(this).children(".one").children(".three").children(".value-version").text();
            let pkg = packageName + "=" + version;
            if (selectedPackages.includes(pkg)) {
                selectedPackages = selectedPackages.filter(item => item !== pkg);
                $(this).children(".one").children(".two").find('i').toggleClass('fa-cube fa-check');
            }
            else {
                selectedPackages.push(pkg);
                $(this).children(".one").children(".two").find('i').toggleClass('fa-cube fa-check');
            }
            deletebtndisp(selectedPackages);
        });
    }

    /*
    This function add an eventlistener to the DOM for showing the delete button only when packages are selected.
    */

    function deletebtndisp(selectedPackages) {
        let n = selectedPackages.length;
        if (n === 0)
            $('#deletebtn').css("display", "none");
        else $('#deletebtn').css("display", "inline");

    }

    return {
        'installed': installed,
        'toinstall': toinstall,
        'selecttoinstall': selecttoinstall,
        'selectinstalled': selectinstalled,
        'deletebtndisp': deletebtndisp
    };
});
