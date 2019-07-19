define(function (require) {
    let $ = require('jquery');
    let dialog = require('base/js/dialog');
    let Jupyter = require('base/js/namespace');
    let utils = require('base/js/utils');
    let scripts = require('./scripts');
    let urls = require('./urls');
    let methods = require('./methods');

    function init(dir) {
        scripts.packageview.load(dir);
        scripts.searchview.load();
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
    }

    function show_button(project) {
        utils.ajax(urls.static_url + 'templates/sidebar.html', {
            dataType: 'html',
            success: function (env_html, status, xhr) {
                // Configure tab
                $('#configure-project-button').click(function (e) {

                    modal = dialog.modal({
                        draggable: false,
                        title: 'Configure Project',
                        body: $.parseHTML(env_html)
                    }).attr('id', 'package-manager-modal').addClass('right full-body');

                    modal.find(".modal-header").unbind("mousedown");

                    modal.on('shown.bs.modal', function (e) {
                        init(project);
                    });

                    modal.on('hidden.bs.modal', function () {
                        scripts.closeview.load();
                    });

                });
            }
        });
    }

    return {
        load_ipython_extension: load,
        show_button: show_button
    };
});
