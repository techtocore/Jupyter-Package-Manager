import $ from 'jquery';
import views from './views';
import api from './api';
import common from './common';

/*
This function populates the sidebar each time it is opened.
*/

function package_view(dir) {

    api.get_info(dir, function (info) {
        var data = info.packages;

        var output = views.installed(data);
        $('#installed-packages').html(output);

        output = views.to_install(data, []);
        $('#to-install').html(output);
        if (output === "") {
            $('#to-install-main').css("display", "none");
        }

        var selectedPackages = [];
        views.select_installed(selectedPackages);

        var toInstall = [];
        views.select_to_install(toInstall);
    });
}


/*
This function populates the dropdown datalist when something is searched.
*/

function search_view() {

    $('#package-name').unbind();

    var typingTimer;                //timer identifier
    var doneTypingInterval = 1000;  //time in ms, 5 second for example

    $('#package-name').on('keyup', function () {
        clearTimeout(typingTimer);
        typingTimer = setTimeout(function () {
            var query = $('#package-name').val();
            if (query.length <= 1) {
                // Do not query if the string size is too small. This will save a lot of time.
                return;
            }
            $('#searchicon').toggleClass('fa-search fa-dot-circle-o').addClass('Blink');
            api.search(query, function (res) {
                var pks = res.packages;
                var html = "";
                $('#searchlist').html(html);
                for (var i = 0; i < pks.length; i++) {
                    var element = pks[i];
                    var name = element.name;
                    var version = element.version;
                    var entry = name + " - " + version;
                    html += "<option value='" + entry + "'>";
                    html += entry;
                    html += "</option>";
                }
                $('#searchicon').toggleClass('fa-search fa-dot-circle-o').removeClass('Blink');
                $('#searchlist').html(html);

                $('input[list="searchlist"]').each(function () {
                    var elem = $(this),
                        list = $('#searchlist');
                    elem[0].value = elem[0].value.split('=')[0];
                    elem.autocomplete({
                        source: list.children().map(function () {
                            return $(this).text();
                        }).get()
                    });
                });
            })
        }, doneTypingInterval);
    });

    //on keydown, clear the countdown 
    $('#package-name').on('keydown', function () {
        clearTimeout(typingTimer);
    });

    /*
    This function adds the selected package to the list display.
    */

    function add_to_install(val) {
        $('#package-name').val("");
        $('#package-name').blur();
        var a = val.split(' - ');
        var pkg = {
            'name': a[0],
            'version': a[1],
            'staus': ''
        };
        var data = [];
        data.push(pkg);
        var output = views.to_install(data);
        $('#to-install').append(output);
        var toInstall = common.get_to_install();
        views.select_to_install(toInstall);
        $('#to-install-main').css("display", "initial");
    }

    $('#package-name').on('input', function () {
        var userText = $(this).val();

        $("#searchlist").find("option").each(function () {
            if ($(this).val() == userText) {
                add_to_install(userText);
            }
        })
    });

}

export default {
    package_view: package_view,
    search_view: search_view
}
