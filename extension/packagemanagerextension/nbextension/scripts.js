
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
            if (output === "") {
                $('#to-install-main').css("display", "none");
            }

            let selectedPackages = [];
            jQuery(views.selectinstalled(selectedPackages));

            let toInstall = [];
            jQuery(views.selecttoinstall(toInstall));
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

            function addtoinstall(val) {
                document.getElementById('package-name').value = '';
                $('#package-name').blur();
                let a = val.split(' - ');
                let pkg = {
                    'name': a[0],
                    'version': a[1],
                    'staus': ''
                };
                let data = [];
                data.push(pkg);
                let output = views.toinstall(data);
                $('#to-install').append(output);
                let toInstall = sessionStorage.getItem("toInstall");
                if (null === toInstall)
                    toInstall = [];
                else {
                    toInstall = toInstall.split(',');
                    if (toInstall[0].length < 1) toInstall = [];
                }
                jQuery(views.selecttoinstall(toInstall));
                $('#to-install-main').css("display", "initial");
            }

            function onInput(e) {
                var input = e.target;
                var val = input.value;
                var list = input.getAttribute('list');
                var options = document.getElementById(list).childNodes;

                for (var i = 0; i < options.length; i++) {
                    if (options[i].innerText === val) {
                        // An item was selected from the list!
                        // yourCallbackHere()
                        addtoinstall(val);
                        break;
                    }
                }
            }
        }
    };

    var closeview = {
        load: function () {
            jQuery(function () {
                $('.closebtn').click(function () {
                    let arr = []
                    sessionStorage.setItem("toInstall", arr);
                    sessionStorage.setItem("selectedPackages", arr);
                    document.getElementById("mySidenav").style.width = "0";
                });
            });
        }
    };

    return {
        'packageview': packageview,
        'searchview': searchview,
        'closeview': closeview
    };
});
