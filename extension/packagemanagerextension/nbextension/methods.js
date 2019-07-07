
define([
    'jquery',
    './common',
], function ($, common) {
    "use strict";

    var updatepkg = {

        update: function (packages, project) {
            let payload = {};
            payload['project'] = project;
            payload['packages'] = packages;
            let settings = {
                "async": true,
                "crossDomain": true,
                "url": "http://localhost:8888/api/packagemanager/packages",
                "method": "PATCH",
                "headers": {
                    "Content-Type": "application/json",
                    "cache-control": "no-cache",
                },
                "processData": false,
                "data": JSON.stringify(payload)
            };


            return new Promise(resolve => {
                $.ajax(settings).done(function (response) {
                    resolve(response);
                });
            });
        },

        load: function () {
            let update = this.update;
            jQuery(function () {
                $('#updatebtn').click(function () {
                    let selectedPackages = sessionStorage.getItem("selectedPackages").split(',');
                    let project = sessionStorage.getItem("project");
                    // let resp = await update(selectedPackages, project);
                    let html = "<p> The following packages are about to be updated: </p> </br>";
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
                    common.confirm("Update Packages", $.parseHTML(html), "Confirm", update(packages, project), undefined);
                });
            });
        }
    };

    return {
        'updatepkg': updatepkg
    };
});
