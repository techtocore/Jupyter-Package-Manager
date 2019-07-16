define([
    'jquery',
    'base/js/utils',
    'base/js/dialog',
    'base/js/keyboard',
], function ($, utils, dialog, keyboard) {
    "use strict";

    function confirm(title, msg, button_text, callback, input) {
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

        var d;

        if (input !== undefined) {
            opts.open = function () {
                // Upon ENTER, click the OK button.
                input.keydown(function (event) {
                    if (event.which === keyboard.keycodes.enter) {
                        d.find('.btn-primary').first().click();
                        return false;
                    }
                });
                input.focus();
            }
        }
        d = dialog.modal(opts);
    }

    return {
        'confirm': confirm
    };
});
