import $ from 'jquery';
import views from './views';
import api from './api';
import common from './common';

/*
This function populates the sidebar each time it is opened.
*/

function package_view(dir) {

    api.get_info(dir, function (info) {
        let data = info.packages;

        let output = views.installed(data);
        $('#installed-packages').html(output);

        output = views.to_install(data, []);
        $('#to-install').html(output);
        if (output === "") {
            $('#to-install-main').css("display", "none");
        }

        let selectedPackages = [];
        views.select_installed(selectedPackages);

        let toInstall = [];
        views.select_to_install(toInstall);
    });
}


/*
This function executes the given function after the specified timeout.
*/

function delay(fn, ms) {
    let timer = 0;
    return function (...args) {
        clearTimeout(timer);
        timer = setTimeout(fn.bind(this, ...args), ms || 0);
    };
}

/*
This function populates the dropdown datalist when something is searched.
*/

function search_view() {

    $('#package-name').unbind();
    $('#package-name').keyup(delay(function (e) {
        let query = this.value;
        if (query.length <= 1) {
            // Do not query if the string size is too small. This will save a lot of time.
            return;
        }
        $('#searchicon').toggleClass('fa-search fa-dot-circle-o').addClass('Blink');
        api.search(query, function (res) {
            let pks = res.packages;
            let html = "";
            $('#searchlist').html(html);
            Array.from(pks).forEach(element => {
                let name = element.name;
                let version = element.version;
                let entry = name + " - " + version;
                html += "<option value='" + entry + "'>";
                html += entry;
                html += "</option>";
            });
            $('#searchicon').toggleClass('fa-search fa-dot-circle-o').removeClass('Blink');
            $('#searchlist').html(html);

            $('input[list="searchlist"]').each(function () {
                let elem = $(this),
                    list = $('#searchlist');
                elem[0].value = elem[0].value.split('=')[0];
                elem.autocomplete({
                    source: list.children().map(function () {
                        return $(this).text();
                    }).get()
                });
            });
        });
    }, 1000));

    /*
    This function adds the selected package to the list display.
    */

    function add_to_install(val) {
        $('#package-name').val("");
        $('#package-name').blur();
        let a = val.split(' - ');
        let pkg = {
            'name': a[0],
            'version': a[1],
            'staus': ''
        };
        let data = [];
        data.push(pkg);
        let output = views.to_install(data);
        $('#to-install').append(output);
        let toInstall = common.get_to_install();
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

export {
    package_view,
    search_view
}
