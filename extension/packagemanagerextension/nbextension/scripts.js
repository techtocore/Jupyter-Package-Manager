
define([
    'jquery',
    'base/js/utils',
    './common',
    './urls',
], function ($, utils, common, urls) {
    "use strict";

    var packageview = {

        get_info: function (dir) {
            var settings = {
                "async": true,
                "crossDomain": true,
                "url": "http://localhost:8888/api/packagemanager/project_info?project=" + dir,
                "method": "GET",
                "headers": {
                    "Content-Type": "application/json",
                    "cache-control": "no-cache",
                },
                "processData": false,
                "data": ""
            }

            return new Promise(resolve => {
                $.ajax(settings).done(function (response) {
                    resolve(response);
                });
            });
        },

        load: async function (dir) {

            let info = await this.get_info(dir);

            var data = info.packages;

            var output = "";
            $.each(data, function (key, val) {
                output += "<div class='values'>";
                output += "<div class='row one'>";
                output += "<div class='col-sm-10 two'>";
                if (val.status === "installed")
                    output += "<i class='fas fa-box-open'></i> &nbsp;"
                else
                    output += "<i class='fas fa-exclamation-triangle'></i> &nbsp;"
                output += '<span class="value-name">' + val.name + '</span>';
                output += "</div>";
                output += "<div class='col-sm-2 three'>";
                output += '<span class="value-version">' + val.version + '</span>'
                output += "</div>";
                output += "</div>";
                output += "</div>";
            });

            $('#content').html(output);

            var selectedPackages = [];

            jQuery(function () {
                $('.values').click(function () {
                    console.log(selectedPackages);
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

                });
            });
        }
    }
    return {
        'packageview': packageview,
    };
});
