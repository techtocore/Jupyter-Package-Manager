# pylint: disable=C0321

import json
import os
import re
import uuid
import yaml

from subprocess import check_output, CalledProcessError
from packaging.version import parse

from traitlets.config.configurable import LoggingConfigurable
from traitlets import Dict

from os.path import expanduser

MAX_LOG_OUTPUT = 6000

CONDA_EXE = os.environ.get("CONDA_EXE", "conda")  # type: str

# try to match lines of json
JSONISH_RE = r'(^\s*["\{\}\[\],\d])|(["\}\}\[\],\d]\s*$)'


class ProcessHelper(LoggingConfigurable):

    @classmethod
    def pkg_info(self, s):
        '''
        Abstracts unwanted details and normalizes the package JSON
        '''
        return {
            "build_string": s.get("build_string", s.get("build")),
            "name": s.get("name"),
            "version": s.get("version")
        }

    @classmethod
    def pkg_info_status(self, swandata, condadata):
        '''
        Combines the data available in both the lists and determines the status of each package
        '''
        packages = {x['name']: x for x in swandata + condadata}.values()
        for i in packages:
            if i in swandata and i in condadata:
                i['status'] = 'installed'
            elif i in swandata and i not in condadata:
                i['status'] = 'not installed'
            elif i not in swandata and i in condadata:
                i['status'] = 'not synced'
        return packages

    @classmethod
    def conda_execute(self, cmd, *args):
        '''
        Executes the conda command line
        '''
        cmd = CONDA_EXE + ' ' + cmd
        cmdline = cmd.split() + list(args)

        try:
            output = check_output(cmdline)
        except CalledProcessError as exc:
            output = exc.output

        return output.decode("utf-8")

    @classmethod
    def clean_conda_json(self, output):
        '''
        Ensures that only valid JSONs are processed
        '''
        lines = output.splitlines()

        try:
            return json.loads('\n'.join(lines))
        except Exception as err:
            return {"error": err}

        # try to remove bad lines
        lines = [line for line in lines if re.match(JSONISH_RE, line)]

        try:
            return json.loads('\n'.join(lines))
        except Exception as err:
            return {"error": err}
        return {"error": True}

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
    def update_yaml(self, name, packages, directory):
        '''
        Updates the .swanproject file with new metadata
        '''
        directory = directory + ".swanproject"
        data = {'ENV': name}
        data['PACKAGE_INFO'] = packages
        try:
            with open(directory, 'w') as outfile:
                yaml.dump(data, outfile, default_flow_style=False)
        except:
            raise "Can't update .swanproject file"

    @classmethod
    def relativeDir(self, directory):
        '''
        Ensures that all directories are relative to home
        '''
        home = expanduser("~")
        if directory[0] != '/':
            directory = '/' + directory
        if directory[-1] != '/':
            directory = directory + '/'
        return home + directory