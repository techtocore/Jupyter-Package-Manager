def _jupyter_nbextension_paths():
    '''
    Used by 'jupyter nbextension' command to install frontend extension
    '''
    return [dict(
        section="tree",
        # the path is relative to the `extension` directory
        src="js",
        # directory in the `nbextension/` namespace
        dest="packagemanager",
        # _also_ in the `nbextension/` namespace
        require="packagemanager/extension")]


def _jupyter_server_extension_paths():
    '''
    Used by 'jupyter serverextension' command to install web server extension
    '''
    return [{
        "module": "packagemanager.serverextension"
    }]
