import Jupyter from 'base/js/namespace';
import $ from 'jquery';
import dialog from 'base/js/dialog';
import scripts from './scripts';
import methods from './methods';
import baseHTML from './templates/sidebar.html';
import api from './api';
import './templates/sidebar.css';

/*
This function populates all the data onto the sidebar and registers appropriate event handlers.
*/

function init(dir) {
    scripts.package_view(dir);
    scripts.search_view();
    methods.update_packages(dir);
    methods.delete_packages(dir);
    methods.install_packages(dir);
}

/*
This function is the entry point to the extension.
*/

function load_ipython_extension() {
    if (!Jupyter.notebook_list) return;
    console.log('[PACKAGE MANAGER] Loading nbextension');
}

/*
This is the function that will be invoked on clicking the cog button on SWAN.
A new sidebar will be created each time corresponding to the project from where it is called.
*/

function show_button(project) {
    // Configure Sidebar
    var modal = dialog.modal({
        draggable: false,
        title: 'Configure Project',
        body: $.parseHTML(baseHTML)
    }).attr('id', 'package-manager-modal').addClass('right full-body');

    modal.find(".modal-header").unbind("mousedown");

    modal.on('shown.bs.modal', function (e) {
        init(project);
    });
}

/*
This function filters the avaialble kernels and displays only the one corresponding to the current project.
*/

function filter_kernel(project) {
    api.get_info(project, function (info) {
        var env = info.env;

        var arr = $("#new-menu > li").map(function () { return this.id });
        var idList = arr.get();
        for (var i = 0; i < idList.length; i++) {
            if (idList[i].startsWith('kernel-conda-env-swanproject')) {
                $('#' + idList[i]).css("display", "block");
                var name = idList[i].substring(17);
                // The first 17 characters correspond to 'kernel-conda-env-'
                name = name.slice(0, -3);
                // This will remove the '-py' at the end of the string
                if (env != name) {
                    $('#' + idList[i]).css("display", "none");
                }
            }
            if (idList[i].startsWith('kernel-python')) {
                // This hides the default python kernels that might appear
                // TODO: Check for any exceptions and handle accordingly
                $('#' + idList[i]).css("display", "none");
            }
        }
        // This hides the conda root environment
        $('#kernel-conda-root-py').css("display", "none");
        //TODO: Change the display name for the visible kernel to make it user friendly.
    });
}


export {
    load_ipython_extension,
    show_button,
    filter_kernel
}