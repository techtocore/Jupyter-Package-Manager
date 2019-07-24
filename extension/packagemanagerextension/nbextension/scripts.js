
define([
    'jquery',
    './views',
    './api',
    './common'
], function ($, views, api, common) {
    "use strict";

    let packageview = {

        /*
        This function populates the sidebar each time it is opened.
        */

        load: async function (dir) {

            sessionStorage.setItem("project", dir);

            let info = await api.getinfo(dir);
            let data = info.packages;

            let output = views.installed(data);
            $('#installed-packages').html(output);

            output = views.toinstall(data, []);
            $('#to-install').html(output);
            if (output === "") {
                $('#to-install-main').css("display", "none");
            }

            let selectedPackages = [];
            views.selectinstalled(selectedPackages);

            let toInstall = [];
            views.selecttoinstall(toInstall);
        }
    };

    let searchview = {

        /*
        This function executes the given function after the specified timeout.
        */

        delay: function (fn, ms) {
            let timer = 0;
            return function (...args) {
                clearTimeout(timer);
                timer = setTimeout(fn.bind(this, ...args), ms || 0);
            };
        },

        /*
        This function populates the dropdown datalist when something is searched.
        */

        load: function () {
            let delay = this.delay;
            $(function () {
                $('#package-name').unbind();
                $('#package-name').keyup(delay(async function (e) {
                    let query = this.value;
                    $('#searchicon').toggleClass('fa-search fa-spinner');
                    let res = await api.search(query);
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
                    $('#searchicon').toggleClass('fa-search fa-spinner');
                    $('#searchlist').html(html);
                }, 1000));
            });

            document.querySelector('input[list="searchlist"]').addEventListener('input', onInput);

            /*
            This function adds the selected package to the list display.
            */

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
                let toInstall = common.get_to_install();
                if (null === toInstall)
                    toInstall = [];
                else {
                    toInstall = toInstall.split(',');
                    if (toInstall[0].length < 1) toInstall = [];
                }
                let output = views.toinstall(data, toInstall);
                $('#to-install').append(output);

                $(views.selecttoinstall(toInstall));
                $('#to-install-main').css("display", "initial");
            }

            function onInput(e) {
                let input = e.target;
                let val = input.value;
                let list = input.getAttribute('list');
                let options = document.getElementById(list).childNodes;

                for (let i = 0; i < options.length; i++) {
                    if (options[i].innerText === val) {
                        addtoinstall(val);
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
