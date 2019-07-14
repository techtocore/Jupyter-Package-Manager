
define([
    'jquery',
    './common',
], function ($) {
    "use strict";

    function toinstall(data) {
        let output = "";
        $.each(data, function (key, val) {
            if (val.status != "installed") {
                output += "<div class='to-install-values'>";
                output += "<div class='row one'>";
                output += "<div class='col-sm-9 two'>";
                output += "<i class='fas fa-exclamation-triangle'></i> &nbsp;"
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

    function installed(data) {
        let output = "";
        $.each(data, function (key, val) {
            if (val.status === "installed") {
                output += "<div class='installed-values'>";
                output += "<div class='row one'>";
                output += "<div class='col-sm-9 two'>";
                output += "<i class='fas fa-box-open'></i> &nbsp;"
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

    function selecttoinstall(toInstall) {
        $('.to-install-values').click(function () {
            let packageName = $(this).children(".one").children(".two").children(".value-name").text();
            let version = $(this).children(".one").children(".three").children(".value-version").text();
            let pkg = packageName + "=" + version;
            if (toInstall.includes(pkg)) {
                toInstall = toInstall.filter(item => item !== pkg);
                $(this).children(".one").children(".two").find('svg').attr("data-icon", "exclamation-triangle");
            }
            else {
                toInstall.push(pkg);
                $(this).children(".one").children(".two").find('svg').attr("data-icon", "check");
            }
            sessionStorage.setItem("toInstall", toInstall);
        });
    }

    function selectinstalled(selectedPackages) {
        $('.installed-values').click(function () {
            let packageName = $(this).children(".one").children(".two").children(".value-name").text();
            let version = $(this).children(".one").children(".three").children(".value-version").text();
            let pkg = packageName + "=" + version;
            if (selectedPackages.includes(pkg)) {
                selectedPackages = selectedPackages.filter(item => item !== pkg);
                $(this).children(".one").children(".two").find('svg').attr("data-icon", "box-open");
            }
            else {
                selectedPackages.push(pkg);
                $(this).children(".one").children(".two").find('svg').attr("data-icon", "check");
            }
            sessionStorage.setItem("selectedPackages", selectedPackages);
            deletebtndisp(selectedPackages);
        });
    }

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
