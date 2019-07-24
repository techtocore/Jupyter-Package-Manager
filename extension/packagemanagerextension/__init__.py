def _jupyter_nbextension_paths():
    '''
    Used by 'jupyter nbextension' command to install frontend extension
    '''
    return [dict(
        section="tree",
        # the path is relative to the `extension` directory
        src="nbextension",
        # directory in the `nbextension/` namespace
        dest="packagemanagerextension",
        # _also_ in the `nbextension/` namespace
        require="packagemanagerextension/extension")]


def _jupyter_server_extension_paths():
    '''
    Used by 'jupyter serverextension' command to install web server extension
    '''
    return [{
        "module": "packagemanagerextension.serverextension"
    }]
