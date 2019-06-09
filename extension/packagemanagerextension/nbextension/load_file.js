/**
 * Tiny module for asynchronously loading static file.
 * @module load_file
 */

define([
    'require'
], function (
    requirejs
) {
        /**
         * Function to asynchronously load static CSS file.
         * @param {string} name 
         */
        function load_css(name) {
            var link = document.createElement("link");
            link.type = "text/css";
            link.rel = "stylesheet";
            link.href = requirejs.toUrl(name);
            document.getElementsByTagName("head")[0].appendChild(link);
        };

        return {
            'load_css': load_css
        };
    });