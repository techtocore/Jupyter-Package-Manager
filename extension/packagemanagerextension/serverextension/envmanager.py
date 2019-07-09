# pylint: disable=C0321

import json
import os
import re
import uuid
import yaml

from packaging.version import parse
from subprocess import check_output, CalledProcessError
from traitlets.config.configurable import LoggingConfigurable
from traitlets import Dict

# these are the types of environments that can be created
package_map = {
    'python2': 'python=2 ipykernel',
    'python3': 'python=3 ipykernel'
}

CONDA_EXE = os.environ.get("CONDA_EXE", "conda")  # type: str

# try to match lines of json
JSONISH_RE = r'(^\s*["\{\}\[\],\d])|(["\}\}\[\],\d]\s*$)'

class EnvManager(LoggingConfigurable):

    def list_projects(self):
        """List all projects that conda knows about"""
        info = self.clean_conda_json(
            self.conda_execute('info --json'))

        def get_info(env):
            return {
                'name': os.path.basename(env),
                'dir': env
            }

        return {
            "projects": [get_info(env) for env in info['envs'] if "swanproject" in env]
        }

    def create_project(self, directory, type):
        env = uuid.uuid1()
        env = 'swanproject-' + str(env)
        folder = directory[:-1].split('/')[-1]

        if not os.path.exists(directory):
            raise Exception('Project directory not available')
        # try:
        #     swanproj = SwanProject(directory)
        #     res = {'error': 'Project directory already associated with an env'}
        #     return res
        # except:
        #     pass

        packages = package_map[type]
        output = self.conda_execute('create -y -q --json -n', env,
                                              *packages.split(" "))
        resp = self.clean_conda_json(output)

        '''
        The kernel.json file is used by jupyter to recognize the iPython kernels (belonging to different env). 
        It is needed to list down the kernel from the newly created environment corresponding to the project.
        '''
        temp = json.dumps(resp)
        returnDict = json.loads(temp)
        kerneljson = {
            "argv": [returnDict['prefix'] + "/bin/python",   "-m",
                     "ipykernel_launcher",
                     "-f",
                     "{connection_file}"],
            "display_name": "Python (" + folder + ")",
            "language": "python"
        }
        kdir = '.local/share/jupyter/kernels/' + env
        if not os.path.exists(kdir):
            os.makedirs(kdir)
        with open(kdir + '/kernel.json', 'w') as fp:
            json.dump(kerneljson, fp)

        # swanproj = SwanProject(directory, env)
        # swanproj.update_swanproject()

        return resp

    def delete_project(self, env):
        output = self.conda_execute(
            'remove -y -q --all --json -n', env)
        '''
        The corresponding kernel.json file needs to be removed to ensure that only valid kernels
        are shown to the user.
        '''
        kdir = '.local/share/jupyter/kernels/' + env
        os.remove(kdir + '/kernel.json')
        os.rmdir(kdir)
        return self.clean_conda_json(output)

    def package_search(self, q):
        # this method is slow and operates synchronously
        output = self.conda_execute('search --json', q)
        data = self.clean_conda_json(output)

        if 'error' in data:
            # we didn't get back a list of packages, we got a dictionary with
            # error info
            return data

        packages = []

        for entries in data.values():
            max_version = None
            max_version_entry = None

            for entry in entries:
                version = parse(entry.get("version", ""))

                if max_version is None or version > max_version:
                    max_version = version
                    max_version_entry = entry

            packages.append(max_version_entry)

        return {"packages": sorted(packages, key=lambda entry: entry.get("name"))}

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
    def clean_conda_json(self, inputjson):
        '''
        Ensures that only valid JSONs are processed
        '''
        lines = inputjson.splitlines()

        try:
            return json.loads('\n'.join(lines))
        except Exception as err:
            raise Exception(err)

        # try to remove bad lines
        lines = [line for line in lines if re.match(JSONISH_RE, line)]

        try:
            cleanJson = json.loads('\n'.join(lines))
        except Exception as err:
            raise Exception(err)
        return cleanJson