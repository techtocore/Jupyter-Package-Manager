import dialog from 'base/js/dialog';
import $ from 'jquery';

/*
This function is responsible for the generation of confirmation modals.
*/

function confirm(title, msg, button_text, callback) {
    var buttons = { Cancel: {} };
    buttons[button_text] = {
        class: 'btn-danger btn-primary',
        click: callback
    };

    var opts = {
        title: title,
        body: msg,
        buttons: buttons
    };

    dialog.modal(opts);
}

/*
This function is responsible for the generation of alert/info modals.
*/

function display_msg(title, msg) {
    var buttons = { Cancel: {} };

    var opts = {
        title: title,
        body: msg,
        buttons: buttons
    };

    dialog.modal(opts);
}

/*
Auxiliary function for checking the DOM for selected packages.
*/

function get_from_list(list) {
    var arr = [];
    for (var i = 0; i < list.length; i++) {
        var element = list[i];
        var val = $(element).children(".two").find('i');
        var classes = $(val).attr('class').split(' ');
        if (classes.includes('fa-check')) {
            var packageName = $(element).find(".two .value-name").text();
            var version = $(element).find(".three .value-version").text();
            var pkg = packageName + "=" + version;
            arr.push(pkg);
        }
    }
    return arr;
}

/*
These functions return the list of currently selected packages.
*/

function get_to_install() {
    var list = $(".to-install-values .one");
    return get_from_list(list);
}

function get_selected_packages() {
    var list = $(".installed-values .one");
    return get_from_list(list);
}

export default {
    confirm: confirm,
    get_selected_packages: get_selected_packages,
    get_to_install: get_to_install,
    display_msg: display_msg
}
