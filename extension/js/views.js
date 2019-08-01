import $ from 'jquery';
import list_item from './templates/list_item.html'

/*
This function generates the DOM for displaying packages that are selected for installation.
*/

function to_install(data) {
    var output = $("<div/>");
    for (var i = 0; i < data.length; i++) {
        var val = data[i];
        if (val.status != "installed") {
            var item = $.parseHTML(list_item);
            $(item).addClass('to-install-values');
            $(item).find('.list_icon').addClass('fa-check');
            $(item).find('.value-name').text(val.name);
            $(item).find('.value-version').text(val.version);
            $(output).append(item);
        }
    }
    return output;
}

/*
This function generates the DOM for displaying packages that are currently installed.
*/

function installed(data) {
    var output = $("<div/>");
    for (var i = 0; i < data.length; i++) {
        var val = data[i];
        if (val.status === "installed") {
            var item = $.parseHTML(list_item);
            $(item).addClass('installed-values');
            $(item).find('.list_icon').addClass('fa-cube');
            $(item).find('.value-name').text(val.name);
            $(item).find('.value-version').text(val.version);
            $(output).append(item);
        }

    }
    return output;
}

function remove_element(array, elem) {
    var index = array.indexOf(elem);
    if (index > -1) {
        array.splice(index, 1);
    }
}

function get_pkg(element) {
    var packageName = $(element).find(".one .two .value-name").text();
    var version = $(element).find(".one .three .value-version").text();
    return packageName + "=" + version;
}

/*
This function add an eventlistener to the DOM for handling packages that are selected for installation.
*/

function select_to_install(toInstall) {
    $('.to-install-values').unbind();
    $('.to-install-values').hover(function () {
        $(this).find(".one .two i").toggleClass('fa-close');
    });
    $('.to-install-values').click(function () {
        var pkg = get_pkg(this);
        if (toInstall.includes(pkg)) {
            remove_element(toInstall, pkg);
            $(this).remove();
        }
        if (toInstall.length === 0) {
            $('#to-install-main').css("display", "none");
        }
    });
}

/*
This function add an eventlistener to the DOM for handling packages that are currently installed.
*/

function select_installed(selectedPackages) {
    $('.installed-values').unbind();
    $('.installed-values').click(function () {
        var pkg = get_pkg(this);
        if (selectedPackages.includes(pkg)) {
            remove_element(selectedPackages, pkg);
            $(this).find(".one .two i").toggleClass('fa-cube fa-check');
        }
        else {
            selectedPackages.push(pkg);
            $(this).find(".one .two i").toggleClass('fa-cube fa-check');
        }
        delete_btn_disp(selectedPackages);
    });
}

/*
This function add an eventlistener to the DOM for showing the delete button only when packages are selected.
*/

function delete_btn_disp(selectedPackages) {
    var n = selectedPackages.length;
    if (n === 0)
        $('#deletebtn').css("display", "none");
    else $('#deletebtn').css("display", "inline");

}

export default {
    installed: installed,
    to_install: to_install,
    select_to_install: select_to_install,
    select_installed: select_installed,
    delete_btn_disp: delete_btn_disp
}