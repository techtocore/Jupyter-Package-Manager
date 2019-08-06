# pylint: disable=C0321

import os
import yaml

from traitlets.config.configurable import LoggingConfigurable
from os.path import expanduser

try:
    from .envmanager import EnvManager
except:
    from envmanager import EnvManager

class SwanProject(LoggingConfigurable):
    '''
    This class represents the in-memory form of the swanproject file
    '''

    def __init__(self, directory):
        directory = self.__relative_dir(directory) + ".swanproject"
        self.directory = directory
        self.env = ""
        self.packages = {}
        try:
            filecontent = yaml.load(open(directory))
            env = filecontent['ENV']
            packages = filecontent['PACKAGE_INFO']
            self.packages = packages
            self.env = env
        except:
            pass

    def update_yaml(self):
        '''
        Updates the .swanproject file with new metadata
        '''
        directory = self.directory
        data = {'ENV': self.env, 'PACKAGE_INFO': self.packages}
        try:
            with open(directory, 'w') as outfile:
                yaml.dump(data, outfile, default_flow_style=False)
        except:
            raise Exception("Can't update .swanproject file")

    def __relative_dir(self, directory):
        '''
        Ensures that all directories are relative to home
        '''
        home = expanduser("~")
        if directory[0] != '/':
            directory = '/' + directory
        if directory[-1] != '/':
            directory = directory + '/'
        return home + directory

    def clear_yaml(self):
        # Clear the contents of the .swanproject file
        open(self.directory, 'w').close()
