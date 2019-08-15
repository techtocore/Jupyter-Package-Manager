import $ from 'jquery';
import endpoints from './api_endpoints.json';

var api_url = (Jupyter.notebook_list || Jupyter.notebook).base_url + "api/packagemanager/";

function get_cookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Check if this cookie string begin with the name we want
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/*
This function makes the API calls to the specified endpoint with the corresponding headers
*/

function api_call(endpoint, url, payload, success) {

    var settings = {
        url: api_url + endpoint.uri + url,
        method: endpoint.method,
        headers: {
            "Content-Type": "application/json",
            "cache-control": "no-cache",
            "X-CSRFToken": get_cookie('_xsrf')
        },
        processData: false,
        success: success
    };

    // Send the payload only if it is not empty

    if (!(Object.keys(payload).length === 0 && payload.constructor === Object)) {
        settings.data = JSON.stringify(payload);
    }

    $.ajax(settings);
}

/*
This function updates all the selected packages.
*/

function update_packages(packages, project) {
    var payload = {
        'project': project,
        'packages': packages
    };
    api_call(endpoints.update_packages, "", payload);
}

/*
This function checks for updates in the selected project.
*/

function check_update(project, success) {
    api_call(endpoints.checkupdate, project, {}, success);
}

/*
This function removes all the selected packages.
*/

function delete_packages(packages, project) {
    var payload = {
        'project': project,
        'packages': packages
    };
    api_call(endpoints.delete_packages, "", payload);
}

function install_packages(packages, project) {
    var payload = {
        'project': project,
        'packages': packages
    };
    api_call(endpoints.install_packages, "", payload);
}

/*
This function returns the status of all the packages in a project.
*/

function get_info(dir, success) {
    api_call(endpoints.getinfo, dir, {}, success);
}

/*
This function lets users search using any input query.
*/

function search(query, success) {
    api_call(endpoints.search, query, {}, success);
}

export default {
    update_packages: update_packages,
    install_packages: install_packages,
    delete_packages: delete_packages,
    get_info: get_info,
    search: search,
    check_update: check_update
}