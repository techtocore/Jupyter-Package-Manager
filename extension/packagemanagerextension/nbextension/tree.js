define(function (require) {
    var $ = require('jquery');
    var Jupyter = require('base/js/namespace');
    var utils = require('base/js/utils');
    var scripts = require('./scripts');
    var urls = require('./urls');
    var methods = require('./methods');

    function init(dir) {
        scripts.packageview.load(dir);
        scripts.searchview.load();
        scripts.closeview.load();
        methods.updatepkg.load();
        methods.deletepkg.load();
        methods.installpkg.load();
    };


    function load() {
        if (!Jupyter.notebook_list) return;

        $('head').append(
            $('<link>')
                .attr('rel', 'stylesheet')
                .attr('type', 'text/css')
                .attr('href', urls.static_url + 'sidebar.css')
        );
        $('head').append(
            $('<script>')
                .attr('src', urls.static_url + 'js/all.js')
        );


        utils.ajax(urls.static_url + 'sidebar.html', {
            dataType: 'html',
            success: function (env_html, status, xhr) {
                // Configure Conda tab
                $(".tab-content").append($(env_html));
                $("#tabs").append(
                    $('<li>')
                        .append(
                            $('<a>')
                                .attr('id', 'package_manager_tab')
                                .text('Package Manager')
                                .css('cursor', 'pointer')
                                .click(function (e) {
                                    document.getElementById("mySidenav").style.width = "440px";
                                    let dir = "/MySwanProjectA"
                                    init(dir);
                                })
                        )
                );
            }
        });

        utils.ajax(urls.static_url + 'packageview.html', {
            dataType: 'html',
            success: function (html, status, xhr) {
                // Configure Conda tab
                $("#packageview").append($(html));
            }
        });

    }
    return {
        load_ipython_extension: load
    };
});
