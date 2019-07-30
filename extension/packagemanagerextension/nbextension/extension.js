import Jupyter from 'base/js/namespace';
import $ from 'jquery';
import dialog from 'base/js/dialog';
import utils from 'base/js/utils';
import scripts from './scripts';
import urls from './urls';
import methods from './methods';

/*
This function populates all the data onto the sidebar and registers appropriate event handlers.
*/

function init(dir) {
    scripts.package_view(dir);
    scripts.search_view();
    methods.update_packages(dir);
    methods.delete_packages(dir);
    methods.install_packages(dir);
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
    show_button
};