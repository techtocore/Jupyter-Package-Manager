define(["base/js/namespace"], function(Jupyter){
    var base_url = (Jupyter.notebook_list || Jupyter.notebook).base_url;
    var api_url = base_url + "api/packagemanager/";
    var static_url = base_url + "nbextensions/packagemanagerextension/";

    return {
        base_url: base_url,
        api_url: api_url,
        static_url: static_url
    };
});
