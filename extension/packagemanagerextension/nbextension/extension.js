/**
 * Entrpoint module for Jupyter Notebook frontend extension.
 * To enable this use "jupyter nbextension enable frontend/extension --section tree" and
 * "jupyter nbextension enable frontend/extension --section notebook"
 * @module extension
 */

define([
	'base/js/namespace',
	'./load_file',
	'./cellqueue',
	'jquery'

], function (
	Jupyter,
	load_file,
	CurrentCell,
	$
) {

		/**
         * Insert Package Manager tab in tree.
         */
		function insert_tab() {
			var tab_text = 'Package Manager';
			var tab_id = 'package_manager';
			var content = 'Package Manager';

			$('<div/>')
				.attr('id', tab_id)
				.append(content)
				.addClass('tab-pane')
				.appendTo('.tab-content')
				.css("display", "none");

			var tab_link = $('<a>')
				.text(tab_text)
				.attr('href', '#' + tab_id)
				.attr('data-toggle', 'tab')
				.on('click', function (evt) {
					window.history.pushState(null, null, '#' + tab_id);
				});

			$('<li>')
				.append(tab_link)
				.appendTo('#tabs');

			if (window.location.hash == '#' + tab_id) {
				tab_link.click();
			}
			$('a').click(function () {
				if (window.location.hash == '#' + tab_id) {
					$('#package_manager').css("display", "block");
				}
				else {
					$('#package_manager').css("display", "none");
				}
			});
			// $('#package_manager').show();
		}

		/**
		 * Entrypoint function : Jupyter automatically detects and call this function.
		 */
		function load_ipython_extension() {
			if (Jupyter.notebook != null) {
				// This is notebook
				console.log('PackageManager: Loading frontend extension');
				load_file.load_css('./static/style.css');
				CurrentCell.register();
			}
			else {
				// This is tree
				console.log('Loading PackageManager Tab Extension')
				load_file.load_css('./static/treetab.css');
				insert_tab();
			}
		}
		return {
			load_ipython_extension: load_ipython_extension
		};
	});