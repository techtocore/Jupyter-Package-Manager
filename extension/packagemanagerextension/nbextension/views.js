
define([
    'jquery',
    'base/js/utils',
    './common',
    './models',
], function ($, utils, common, models) {
    "use strict";

    function action_start(btn) {
        var $btn = $(btn);
        $btn.focus();

        var $icon = $btn.find('i');
        var old_classes = $icon.attr('class');
        $icon.attr('class', 'fa fa-spinner fa-spin');
        return old_classes;
    }

    function action_end(btn, old_classes) {
        var $btn = $(btn);
        $btn.blur();
        $btn.find('i').attr('class', old_classes);
    }

    var ListView = {
        selector: null,
        model: null,
        columns: [],      // e.g., [{ heading: 'Name', attr: 'name', width: 3 }]
        label: 'item',
        selectable: true,
        transforms: {},
        bindings: {},

        init: function () {
            this.create_header();
            this.bind();
        },

        bind: function () {
            var $root = $(this.selector);

            $.each(this.bindings, function (selector, callback) {
                $root.find(selector).click(callback);
            });

            $root.find("button[title]").tooltip({
                container: "body",
                placement: "top"
            });
        },

        update_label: function (count) {
            $(this.selector).find('.toolbar_info').text(common.pluralize(count, this.label));
        },

        create_header: function (count) {
            var $header = $(this.selector).find('.list_header');
            $header.empty();

            $.each(this.columns, function (index, column) {
                $('<div/>')
                    .addClass('col-xs-' + column.width)
                    .text(column.heading)
                    .appendTo($header);
            });
        },

        refresh: function (data) {
            var that = this;
            var $root = $(this.selector);

            this.update_label(data.length);
            var $body = $root.find('.list_body');
            $body.empty();

            $.each(data, function (index, row) {
                var $row = $('<div/>')
                    .addClass('list_item')
                    .addClass('row')
                    .data('data', row);

                $.each(that.columns, function (index, column) {
                    var $cell = $('<div/>')
                        .addClass('col-xs-' + column.width);

                    var xform = that.transforms[column.attr];
                    if (xform) {
                        $cell.append(xform(row, $row));
                    }
                    else {
                        // Default is to stuff text in the div
                        $cell.text(row[column.attr]);
                    }

                    // Create selection checkbox, if needed
                    if (that.selectable && index === 0) {
                        var selected_box = $('<input/>')
                            .attr('type', 'checkbox')
                            .attr('title', 'Click to select')
                            .addClass('flush-left')
                            .click(function () { row.selected = !row.selected; })
                            .prependTo($cell);
                    }

                    $row.append($cell);
                });

                $body.append($row);
            });
        }
    }

    var EnvView = Object.create(ListView);

    function new_env_prompt(callback) {
        var input = $('<input id="env_name" name="name"/>');
        var dialogform = $('<div/>').attr('title', 'Create New Project').append(
            $('<form class="new_env_form"/>').append(
                $('<fieldset/>')
                    .append($('<label for="env_name">Project Directory:</label>'))
                    .append(input)
                    .append($('<label for="env_type">Type:</label>'))
                    .append($('<select id="env_type" name="type">' +
                        '<option value="python2">Python 2</option>' +
                        '<option selected value="python3">Python 3</option>' +
                        '</select>'))
            )
        );

        function ok() {
            callback($('#env_name').val(), $('#env_type').val());
        }

        common.confirm('New Project', dialogform, 'Create', ok, input);
    }

    $.extend(EnvView, {
        selector: '#environments',
        label: 'SWAN Projects',
        selectable: false,
        model: models.environments,
        columns: [
            { heading: 'Action', attr: '_action', width: 1 },
            { heading: 'Name', attr: 'name', width: 5 },
            { heading: 'Directory', attr: 'dir', width: 6 },
        ],

        transforms: {
            name: function (row) {
                return common.link('#', row.name)
                    .click(function () {
                        models.environments.select(row)
                    });
            },

            is_default: function (row) {
                return $('<div class="default_col">').append(common.icon(row.is_default ? 'check' : ''));
            },

            _action: function (row, $row) {
                // This is a pseudo-attribute

                function ActionMessage(msg) {
                    var $replacement = $('<div class="inprogress"/>').text(msg);
                    $row.find('.action_col').replaceWith($replacement);
                }

                return $('<span class="action_col"/>')
                    .addClass('btn-group')
                    .append(common.icon('trash-o').click(function () {
                        alert("Feature Currently Disabled")
                    }));
            }
        },

        bindings: {
            '#new_env': function () {
                var btn = this;

                new_env_prompt(function (name, type) {
                    var btn_state = action_start(btn);
                    models.environments.create(name, type).then(function () {
                        action_end(btn, btn_state);
                    });
                });
            },
            '#refresh_env_list': function () {
                var btn = this;
                var btn_state = action_start(btn);

                models.environments.load().then(function () {
                    action_end(btn, btn_state);
                });
            },
        }
    });

    var AvailView = Object.create(ListView);

    $.extend(AvailView, {
        selector: '#available_packages',
        label: 'available package',

        columns: [
            { heading: 'Name', attr: 'name', width: 5 },
            { heading: 'Version', attr: 'version', width: 2 },
            { heading: 'Channel', attr: 'channel', width: 5 }
        ],

        bind: function () {
            ListView.bind.call(this);

            var that = this;
            var $box = $('#searchboxi');

            $box.keyup(function () {
                that.filter($box.val());
            });
        },

        refresh: function (data) {
            ListView.refresh.call(this, data);

            var $box = $('#searchboxi');
            this.filter($box.val());
        },

        bindings: {
            '#refresh_avail_list': function () {
                var btn = this;
                var btn_state = action_start(btn);

                models.available.load().then(function () {
                    action_end(btn, btn_state);
                });
            }
        },

        filter: function (query) {
            var count = 0;

            $(this.selector).find('.list_item').each(function (index, elem) {
                var $elem = $(elem);

                if ($elem.data('data').name.indexOf(query) === -1) {
                    $elem.hide();
                }
                else {
                    $elem.show();
                    count++;
                }
            });

            this.update_label(count);
        }
    });

    var InstalledView = Object.create(ListView);

    $.extend(InstalledView, {
        selector: '#installed_packages',
        label: 'installed package',

        columns: [
            { heading: 'Name', attr: 'name', width: 5 },
            { heading: 'Version', attr: 'version', width: 2 },
            { heading: 'Build', attr: 'build', width: 2 },
            { heading: 'Available', attr: 'available', width: 3 }
        ],

        update_label: function (count) {
            $(this.selector)
                .find('.toolbar_info')
                .text(common.pluralize(count, this.label) +
                    ' in environment "' + models.environments.selected.name + '"');
        },

        bindings: {
            '#refresh_pkg_list': function () {
                var btn = this;
                var btn_state = action_start(btn);

                models.installed.load().then(function () {
                    action_end(btn, btn_state);
                });
            }

        },
    });

    return {
        'EnvView': EnvView,
        'AvailView': AvailView,
        'InstalledView': InstalledView
    };
});
