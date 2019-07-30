import dialog from 'base/js/dialog';
import $ from 'jquery';

/*
This function is responsible for the generation of confirmation modals.
*/

function confirm(title, msg, button_text, callback) {
    let buttons = { Cancel: {} };
    buttons[button_text] = {
        class: 'btn-danger btn-primary',
        click: callback
    };

    let opts = {
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
    let buttons = { Cancel: {} };

    let opts = {
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
    let arr = [];
    for (let element of list) {
        let val = $(element).children(".two").find('i');
        let classes = $(val).attr('class').split(' ');
        if (classes.includes('fa-check')) {
            let packageName = $(element).find(".two .value-name").text();
            let version = $(element).find(".three .value-version").text();
            let pkg = packageName + "=" + version;
            arr.push(pkg);
        }
    }
    return arr;
}

/*
These functions return the list of currently selected packages.
*/

function get_to_install() {
    let list = $(".to-install-values .one");
    return get_from_list(list);
}

function get_selected_packages() {
    let list = $(".installed-values .one");
    return get_from_list(list);
}

export default{
    confirm: confirm,
    get_selected_packages: get_selected_packages,
    get_to_install: get_to_install,
    display_msg: display_msg
}
