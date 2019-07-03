
define([
    'jquery',
    'base/js/utils',
    './common',
    './urls',
], function ($, utils, common, urls) {
    "use strict";

    var packageview = {
        load: function () {
            var data = [
                {
                    "name": "Formatting",
                    "version": "2.0.2"
                },
                {
                    "name": "Pandas",
                    "version": "4.6"
                },
                {
                    "name": "Datatables",
                    "version": "5.0.1"
                },
                {
                    "name": "Tensorflow",
                    "version": "2.1.4"
                }
            ];

            var output = "";
            $.each(data, function (key, val) {
                output += "<div class='values'>";
                output += "<div class='row one'>";
                output += "<div class='col-sm-10 two'>";
                output += "<i class='fas fa-box-open'></i> &nbsp;"
                output += '<span class="value-name">' + val.name + '</span>';
                output += "</div>";
                output += "<div class='col-sm-2 three'>";
                output += '<span class="value-version">' + val.version + '</span>'
                output += "</div>";
                output += "</div>";
                output += "</div>";
            });

            $('#content').html(output);

            /* SEEKER FUNCTION */
            if (!RegExp.escape) {
                RegExp.escape = function (s) {
                    return s.replace(/[\-\[\]{}()*+?.,\\\^$|#\s]/g, "\\$&")
                };
            }

            jQuery(function () {
                var $rows = $('.values');
                $('#package-name').keyup(function () {
                    var regex = new RegExp(RegExp.escape($.trim(this.value).replace(/\s+/g, ' ')), 'i')
                    $rows.hide().filter(function () {
                        var text = $(this).children(".one").children(".two").children(".value-name").text().replace(/\s+/g, ' ');
                        return regex.test(text)
                    }).show();
                });
            });

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
