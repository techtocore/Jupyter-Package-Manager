
define([
    'jquery',
    './views',
], function ($, views) {
    "use strict";

    var packageview = {

        get_info: function (dir) {
            let settings = {
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
            };

            return new Promise(resolve => {
                $.ajax(settings).done(function (response) {
                    resolve(response);
                });
            });
        },

        load: async function (dir) {

            sessionStorage.setItem("project", dir);

            let info = await this.get_info(dir);
            let data = info.packages;

            let output = views.installed(data);
            $('#installed-packages').html(output);

            output = views.toinstall(data);
            $('#to-install').html(output);


            let selectedPackages = [];

            jQuery(function () {
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
                });
            });

            let toInstall = [];

            jQuery(function () {
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
            });
        }
    };

    var searchview = {

        search: function (query) {
            let settings = {
                "async": true,
                "crossDomain": true,
                "url": "http://localhost:8888/api/packagemanager/packages/search?q=" + query,
                "method": "GET",
                "headers": {
                    "cache-control": "no-cache"
                }
            };

            return new Promise(resolve => {
                $.ajax(settings).done(function (response) {
                    resolve(response);
                });
            });
        },

        delay: function (fn, ms) {
            let timer = 0;
            return function (...args) {
                clearTimeout(timer);
                timer = setTimeout(fn.bind(this, ...args), ms || 0);
            };
        },

        load: function () {
            let delay = this.delay;
            let search = this.search;
            jQuery(function () {
                $('#package-name').keyup(delay(async function (e) {
                    let query = this.value;
                    let res = await search(query);
                    let pks = res.packages;
                    let html = ""
                    $('#searchlist').html(html);
                    Array.from(pks).forEach(element => {
                        let name = element.name;
                        let version = element.version;
                        let entry = name + " - " + version;
                        html += "<option value='" + entry + "'>";
                        html += entry;
                        html += "</option>";
                    });
                    $('#searchlist').html(html);
                }, 1000));
            });

            document.querySelector('input[list="searchlist"]').addEventListener('input', onInput);

            function onInput(e) {
                var input = e.target;
                var val = input.value;
                var list = input.getAttribute('list');
                var options = document.getElementById(list).childNodes;

                for (var i = 0; i < options.length; i++) {
                    if (options[i].innerText === val) {
                        // An item was selected from the list!
                        // yourCallbackHere()
                        alert('item selected: ' + val);
                        break;
                    }
                }
            }
        }
    };

    return {
        'packageview': packageview,
        'searchview': searchview
    };
});
