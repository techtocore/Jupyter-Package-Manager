define(["base/js/namespace"], function (Jupyter) {
    let base_url = (Jupyter.notebook_list || Jupyter.notebook).base_url;
    let api_url = base_url + "api/packagemanager/";
    let static_url = base_url + "nbextensions/packagemanagerextension/";

    return {
        base_url: base_url,
        api_url: api_url,
        static_url: static_url
    };
});
