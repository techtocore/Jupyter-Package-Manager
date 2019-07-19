define([
    'base/js/dialog',
], function (dialog) {
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

    return {
        'confirm': confirm
    };
});
