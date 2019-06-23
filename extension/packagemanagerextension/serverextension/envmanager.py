# pylint: disable=C0321

import json
import os
import re
import uuid
import yaml

from pkg_resources import parse_version
from subprocess import check_output, CalledProcessError

from traitlets.config.configurable import LoggingConfigurable
from traitlets import Dict


def pkg_info(s):
    try:
        # for conda >= 4.3, `s` should be a dict
        name = s['name']
        version = s['version']
        build = s.get('build_string') or s['build']
    except TypeError:
        # parse legacy string version for information
        name, version, build = s.rsplit('-', 2)

    return {
        'name': name,
        'version': version,
        'build': build
    }


def pkg_info_status(s, names):
    try:
        # for conda >= 4.3, `s` should be a dict
        name = s['name']
        version = s['version']
        build = s.get('build_string') or s['build']
    except TypeError:
        # parse legacy string version for information
        name, version, build = s.rsplit('-', 2)
    status = "not available"
    if name in names:
        status = "installed"
    return {
        'name': name,
        'version': version,
        'build': build,
        "status": status
    }


MAX_LOG_OUTPUT = 6000

# try to match lines of json
JSONISH_RE = r'(^\s*["\{\}\[\],\d])|(["\}\}\[\],\d]\s*$)'

# these are the types of environments that can be created
package_map = {
    'python2': 'python=2 ipykernel',
    'python3': 'python=3 ipykernel'
}


class EnvManager(LoggingConfigurable):
    envs = Dict()

    def _execute(self, cmd, *args):
        cmdline = cmd.split() + list(args)
        self.log.debug('[packagemanagerextension] command: %s', cmdline)

        try:
            output = check_output(cmdline)
        except CalledProcessError as exc:
            self.log.debug(
                '[packagemanagerextension] exit code: %s', exc.returncode)
            output = exc.output

        self.log.debug('[packagemanagerextension] output: %s',
                       output[:MAX_LOG_OUTPUT])

        if len(output) > MAX_LOG_OUTPUT:
            self.log.debug('[packagemanagerextension] ...')

        return output.decode("utf-8")

    def list_envs(self):
        """List all environments that conda knows about"""
        info = self.clean_conda_json(self._execute('conda info --json'))
        default_env = info['default_prefix']

        root_env = {
            'name': 'root',
            'dir': info['root_prefix'],
            'is_default': info['root_prefix'] == default_env
        }

        def get_info(env):
            return {
                'name': os.path.basename(env),
                'dir': env,
                'is_default': env == default_env
            }

        return {
            "environments": [root_env] + [get_info(env) for env in info['envs'] if env != info['root_prefix']]
        }

    def clean_conda_json(self, output):
        lines = output.splitlines()

        try:
            return json.loads('\n'.join(lines))
        except Exception as err:
            self.log.warn(
                '[packagemanagerextension] JSON parse fail:\n%s', err)

        # try to remove bad lines
        lines = [line for line in lines if re.match(JSONISH_RE, line)]

        try:
            return json.loads('\n'.join(lines))
        except Exception as err:
            self.log.error(
                '[packagemanagerextension] JSON clean/parse fail:\n%s', err)

        return {"error": True}

    def delete_project(self, directory):
        env = ""
        directory = str(directory) + ".swanproject"
        try:
            env = yaml.load(open(directory))['ENV']
        except:
            return {'error': "Can't find project"}
        output = self._execute('conda remove -y -q --all --json -n', env)
        return self.clean_conda_json(output)

    def project_info(self, directory):
        env = ""
        names = []
        packagesMD = {}
        directory = str(directory) + ".swanproject"
        try:
            val = yaml.load(open(directory))
            env = val['ENV']
            packagesMD = val['PACKAGE_INFO']
        except:
            return {'error': "Can't find project"}

        for item in packagesMD:
            names.append(item.get('name'))

        output = self._execute('conda list --no-pip --json -n', env)
        data = self.clean_conda_json(output)
        if 'error' in data:
            # we didn't get back a list of packages, we got a dictionary with
            # error info
            return data

        return {
            "env": env,
            "packages": [pkg_info_status(package, names) for package in data]
        }

    def export_env(self, env):
        return self._execute('conda list -e -n', env)

    def clone_env(self, env, name):
        output = self._execute('conda create -y -q --json -n', name,
                               '--clone', env)
        return self.clean_conda_json(output)

    def create_project(self, directory, type):
        name = uuid.uuid1()
        name = 'swanproject-' + str(name)
        data = {'ENV': name}

        if not os.path.exists(directory):
            os.makedirs(directory)

        if os.path.isfile(directory + '.swanproject'):
            res = {'error': 'This directory alreday contains a project'}
            return res

        packages = package_map[type]
        output = self._execute('conda create -y -q --json -n', name,
                               *packages.split(" "))
        packages = self._execute('conda list --no-pip --json -n', name)
        packages = self.clean_conda_json(packages)
        data['PACKAGE_INFO'] = packages
        with open(directory + '.swanproject', 'w') as outfile:
            yaml.dump(data, outfile, default_flow_style=False)
        return self.clean_conda_json(output)

    def env_packages(self, env):
        output = self._execute('conda list --no-pip --json -n', env)
        data = self.clean_conda_json(output)
        if 'error' in data:
            # we didn't get back a list of packages, we got a dictionary with
            # error info
            return data

        return {
            "packages": [pkg_info(package) for package in data]
        }

    def check_update(self, directory, packages):
        env = ""
        directory = str(directory) + ".swanproject"
        try:
            env = yaml.load(open(directory))['ENV']
        except:
            return {'error': "Can't find project"}
        output = self._execute('conda update --dry-run -q --json -n', env,
                               *packages)
        data = self.clean_conda_json(output)

        if 'error' in data:
            # we didn't get back a list of packages, we got a dictionary with
            # error info
            return data
        elif 'actions' in data:
            links = data['actions'].get('LINK', [])
            package_versions = [link.get('dist_name') for link in links]
            return {
                "updates": [pkg_info(pkg_version)
                            for pkg_version in package_versions]
            }
        else:
            # no action plan returned means everything is already up to date
            return {
                "updates": []
            }

    def install_packages(self, directory, packages):
        env = ""
        directory = str(directory) + ".swanproject"
        try:
            env = yaml.load(open(directory))['ENV']
        except:
            return {'error': "Can't find project"}
        output = self._execute('conda install -y -q --json -n', env, *packages)
        data = {'ENV': env}
        packages = self._execute('conda list --no-pip --json -n', env)
        packages = self.clean_conda_json(packages)
        data['PACKAGE_INFO'] = packages
        with open(directory, 'w') as outfile:
            yaml.dump(data, outfile, default_flow_style=False)
        return self.clean_conda_json(output)

    def update_packages(self, directory, packages):
        env = ""
        directory = str(directory) + ".swanproject"
        try:
            env = yaml.load(open(directory))['ENV']
        except:
            return {'error': "Can't find project"}
        output = self._execute('conda update -y -q --json -n', env, *packages)
        data = {'ENV': env}
        packages = self._execute('conda list --no-pip --json -n', env)
        packages = self.clean_conda_json(packages)
        data['PACKAGE_INFO'] = packages
        with open(directory, 'w') as outfile:
            yaml.dump(data, outfile, default_flow_style=False)
        return self.clean_conda_json(output)

    def remove_packages(self, directory, packages):
        env = ""
        directory = str(directory) + ".swanproject"
        try:
            env = yaml.load(open(directory))['ENV']
        except:
            return {'error': "Can't find project"}
        output = self._execute('conda remove -y -q --json -n', env, *packages)
        data = {'ENV': env}
        packages = self._execute('conda list --no-pip --json -n', env)
        packages = self.clean_conda_json(packages)
        data['PACKAGE_INFO'] = packages
        with open(directory, 'w') as outfile:
            yaml.dump(data, outfile, default_flow_style=False)
        return self.clean_conda_json(output)

    def package_search(self, q):
        # this method is slow and operates synchronously
        output = self._execute('conda search --json', q)
        data = self.clean_conda_json(output)

        if 'error' in data:
            # we didn't get back a list of packages, we got a dictionary with
            # error info
            return data

        packages = []

        for name, entries in data.items():
            max_version = None
            max_version_entry = None

            for entry in entries:
                version = parse_version(entry.get('version', ''))

                if max_version is None or version > max_version:
                    max_version = version
                    max_version_entry = entry

            packages.append(max_version_entry)
        return {
            "packages": sorted(packages, key=lambda entry: entry.get('name'))
        }
