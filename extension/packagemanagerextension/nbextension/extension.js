define(function (require) {
    let $ = require('jquery');
    let Jupyter = require('base/js/namespace');
    let utils = require('base/js/utils');
    let scripts = require('./scripts');
    let urls = require('./urls');
    let methods = require('./methods');

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
                .attr('href', urls.static_url + 'templates/sidebar.css')
        );

        utils.ajax(urls.static_url + 'templates/sidebar.html', {
            dataType: 'html',
            success: function (env_html, status, xhr) {
                // Configure tab
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
    }
    return {
        load_ipython_extension: load
    };
});