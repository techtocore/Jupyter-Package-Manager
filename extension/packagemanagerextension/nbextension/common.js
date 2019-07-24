define([
    'base/js/dialog',
    'jquery'
], function (dialog, $) {
    "use strict";

    function confirm(title, msg, button_text, callback) {
        let buttons = { Cancel: {} };
        buttons[button_text] = {
            class: 'btn-danger btn-primary',
            click: callback
        }

        let opts = {
            title: title,
            body: msg,
            buttons: buttons
        };

        dialog.modal(opts);
    }

    function get_to_install() {
        let to_install = [];
        let list = $('.to-install-values').children(".one")
        list.forEach(element => {
            let val = $(element).children(".two").find('i');
            if ($(val).find('.fa-check')[0]) {
                let packageName = $(element).children(".two").children(".value-name").text();
                let version = $(element).children(".three").children(".value-version").text();
                let pkg = packageName + "=" + version;
                to_install.push(pkg);
            }
        });
        return to_install;
    }

    function get_selected_packages() {
        let selected_packages = [];
        let list = $('.installed-values').children(".one")
        list.forEach(element => {
            let val = $(element).children(".two").find('i');
            if ($(val).find('.fa-check')[0]) {
                let packageName = $(element).children(".two").children(".value-name").text();
                let version = $(element).children(".three").children(".value-version").text();
                let pkg = packageName + "=" + version;
                selected_packages.push(pkg);
            }
        });
        return selected_packages;
    }

    return {
        'confirm': confirm,
        'get_selected_packages': get_selected_packages,
        'get_to_install': get_to_install
    };
});
