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
                $("#tree").append($(env_html));
                $(".page-tree").append('<button title="Configure Project" id="configure-project-button" class="btn btn-default btn-xs" style="display: inline-block;"><i class="fa fa-cog"></i></button>');
                $('#configure-project-button').click(function (e) {
                    document.getElementById("mySidenav").style.width = "440px";
                    let dir = location.href.split('/').slice(-1)[0];
                    dir = '/SWAN_projects/' + dir;
                    init(dir);
                })
            }
        });
    }
    return {
        load_ipython_extension: load
    };
});
