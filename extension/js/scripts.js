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
        $('#installed-packages').append(output);

        output = views.to_install(data);
        $('#to-install').append(output);
        if ($(output).children().length === 0) {
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
    var doneTypingInterval = 1500;  //time in ms, 1.5 seconds for example

    $('#package-name').on('keyup', function () {
        clearTimeout(typingTimer);
        typingTimer = setTimeout(function () {
            var query = $('#package-name').val();
            if (query.length <= 1) {
                // Do not query if the string size is too small. This will save a lot of time.
                return;
            }
            $('#searchlist').empty();
            $('#searchicon').toggleClass('fa-search fa-dot-circle-o').addClass('Blink');
            api.search(query, function (res) {
                var pks = res.packages;
                for (var i = 0; i < pks.length; i++) {
                    var element = pks[i];
                    var name = element.name;
                    var version = element.version;
                    var entry = name + " - " + version;
                    var opt = $("<option>").val(entry).text(entry);
                    $('#searchlist').append(opt);
                }
                $('#searchicon').toggleClass('fa-search fa-dot-circle-o').removeClass('Blink');

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
