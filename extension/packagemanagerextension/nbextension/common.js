define([
    'jquery',
    'base/js/utils',
    'base/js/dialog',
    'base/js/keyboard',
], function ($, utils, dialog, keyboard) {
    "use strict";

    function confirm(title, msg, button_text, callback) {
        var buttons = { Cancel: {} };
        buttons[button_text] = {
            class: 'btn-danger btn-primary',
            click: callback
        }

        var opts = {
            title: title,
            body: msg,
            buttons: buttons
        };

        dialog.modal(opts);
    }

    return {
        'confirm': confirm
    };
});
