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
                .attr('href', urls.static_url + 'conda.css')
        );

        utils.ajax(urls.static_url + 'tab.html', {
            dataType: 'html',
            success: function (env_html, status, xhr) {
                // Configure Conda tab
                $(".tab-content").append($(env_html));
                $("#tabs").append(
                    $('<li>')
                        .append(
                            $('<a>')
                                .attr('id', 'package_manager_tab')
                                .attr('href', '#package_manager_html_id')
                                .attr('data-toggle', 'tab')
                                .text('Package Manager')
                                .click(function (e) {
                                    window.history.pushState(null, null, '#package_manager_html_id');
                                    models.environments.load();
                                    models.available.load();
                                })
                        )
                );

                views.EnvView.init();
                views.AvailView.init();
                views.InstalledView.init();

                models.environments.view = views.EnvView;
                models.available.view = views.AvailView;
                models.installed.view = views.InstalledView;

                if (window.location.hash === '#package_manager_html_id') {
                    $('#package_manager_tab').click();
                }
            }
        });
    }
    return {
        load_ipython_extension: load
    };
});
