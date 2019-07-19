
define([
], function () {
    "use strict";

    return {
        "updatep": {
            "uri": "packages",
            "method": "PATCH"
        },
        "checkupdate": {
            "uri": "packages/check_update?project=",
            "method": "GET"
        },
        "deletep": {
            "uri": "packages",
            "method": "DELETE"
        },
        "installp": {
            "uri": "packages",
            "method": "POST"
        },
        "getinfo": {
            "uri": "project_info?project=",
            "method": "GET"
        },
        "search": {
            "uri": "packages/search?q=",
            "method": "GET"
        }
    };
});
