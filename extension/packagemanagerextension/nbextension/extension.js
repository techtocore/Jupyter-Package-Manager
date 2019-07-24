define([
    'base/js/namespace',
    'jquery',
    'base/js/dialog',
    'base/js/utils',
    './scripts',
    './urls',
    './methods'
], function (Jupyter, $, dialog, utils, scripts, urls, methods) {

    /*
    This function populates all the data onto the sidebar and registers appropriate event handlers.
    */

    function init(dir) {
        scripts.packageview(dir);
        scripts.searchview();
        methods.updatepkg();
        methods.deletepkg();
        methods.installpkg();
    };

    /*
    This function is the entry point to the extension. It loads the custom CSS files.
    */

    function load() {
        if (!Jupyter.notebook_list) return;

        $('head').append(
            $('<link>')
                .attr('rel', 'stylesheet')
                .attr('type', 'text/css')
                .attr('href', urls.static_url + 'templates/sidebar.css')
        );
    }

    /*
    This is the function that will be invoked on clicking the cog button on SWAN.
    A new sidebar will be created each time corresponding to the project from where it is called.
    */

    function show_button(project) {
        utils.ajax(urls.static_url + 'templates/sidebar.html', {
            dataType: 'html',
            success: function (env_html) {
                // Configure Sidebar
                modal = dialog.modal({
                    draggable: false,
                    title: 'Configure Project',
                    body: $.parseHTML(env_html)
                }).attr('id', 'package-manager-modal').addClass('right full-body');

                modal.find(".modal-header").unbind("mousedown");

                modal.on('shown.bs.modal', function (e) {
                    init(project);
                });

            }
        });
    }

    return {
        load_ipython_extension: load,
        show_button: show_button
    };
});
