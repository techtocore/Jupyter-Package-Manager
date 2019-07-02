define(function (require) {
    var $ = require('jquery');
    var Jupyter = require('base/js/namespace');
    var utils = require('base/js/utils');
    var models = require('./models');
    var views = require('./views');
    var urls = require('./urls');

    function load() {
        if (!Jupyter.notebook_list) return;
        var base_url = Jupyter.notebook_list.base_url;
        $('head').append(
            $('<link>')
                .attr('rel', 'stylesheet')
                .attr('type', 'text/css')
                .attr('href', urls.static_url + 'sidebar.css')
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
                                .click(function (e) {
                                    document.getElementById("mySidenav").style.width = "450px";
                                })
                        )
                );
            }
        });

        utils.ajax(urls.static_url + 'projectinfo.html', {
            dataType: 'html',
            success: function (html, status, xhr) {
                // Configure Conda tab
                $("#projectinfo").append($(html));
            }
        });

        utils.ajax(urls.static_url + 'installpackage.html', {
            dataType: 'html',
            success: function (html, status, xhr) {
                // Configure Conda tab
                $("#installpackage").append($(html));
                models.available.load();
                views.AvailView.init();
                models.available.view = views.AvailView;
            }
        });

    }
    return {
        load_ipython_extension: load
    };
});
