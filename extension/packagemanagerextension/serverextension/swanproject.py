# pylint: disable=C0321

import yaml

from traitlets.config.configurable import LoggingConfigurable

from .processhelper import ProcessHelper
process_helper = ProcessHelper()

class SwanProject(LoggingConfigurable):

    @classmethod
    def get_swanproject(self, directory):
        '''
        Directory to env mapping
        '''
        directory = directory + ".swanproject"
        try:
            env = yaml.load(open(directory))['ENV']
        except:
            raise "Can't find project"
        return env

    @classmethod
    def update_swanproject(self, directory):
        '''
        Update the .swanproject file with the updated metadata
        '''
        env = self.get_swanproject(directory)
        packages = process_helper.conda_execute('list --json -n', env)
        packages = process_helper.clean_conda_json(packages)
        process_helper.update_yaml(env, packages, directory)