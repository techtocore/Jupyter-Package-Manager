
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


    return {
        'installed': installed,
        'toinstall': toinstall
    };
});
