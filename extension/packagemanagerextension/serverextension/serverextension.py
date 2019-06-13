from notebook.base.handlers import IPythonHandler
import sys
import os
import subprocess
import json

# For now write logs in ~/packgeManager-monitoring.txt
sys.stdout = open(os.path.join(os.path.expanduser('~'),
                               'packgeManager-monitoring.txt'), 'w')


class PackageManagerHandler(IPythonHandler):

    def get(self):
        """
        This method handles all the `GET` requests recieved on the server extension. 
        """
        action = str(self.get_argument('action', 'none'))

        if action == 'list_info':
            self.list_info()
            return

        if action == 'pip_list':
            self.pip_list()
            return

        if action == 'conda_list':
            env = str(self.get_argument('env', 'none'))
            self.conda_list(env)
            return

        result = 'API Status: Live'
        self.send_to_client(result)
        return

    def post(self):
        """
        This method handles all the `POST` requests recieved on the server extension. 
        """
        action = str(self.get_body_argument('action', 'none'))

        if action == 'install':
            name = str(self.get_body_argument('name', 'none'))
            version = str(self.get_body_argument('version', 'none'))
            env = str(self.get_body_argument('env', 'none'))
            self.install(name, env, version)

        result = 'API Status: Live'
        self.send_to_client(result)
        return

    def delete(self):
        """
        This method handles all the `DELETE` requests recieved on the server extension. 
        """
        action = str(self.get_body_argument('action', 'none'))

        if action == 'uninstall':
            name = str(self.get_body_argument('name', 'none'))
            env = str(self.get_body_argument('env', 'none'))
            self.uninstall(name, env)

        result = 'API Status: Live'
        self.send_to_client(result)
        return

    def list_info(self):
        info = subprocess.check_output(["conda", "info", "--json"])
        json_str = json.dumps(info)
        self.send_to_client(json.loads(json_str))

    def pip_list(self):
        info = subprocess.check_output(["pip", "list", "--format=json"])
        json_str = json.dumps(info)
        self.send_to_client(json.loads(json_str))

    def conda_list(self, env):
        if env == "none":
            info = subprocess.check_output(["conda", "list", "--json"])
        else:
            info = subprocess.check_output(
                ["conda", "list", "-n", env, "--json"])
        json_str = json.dumps(info)
        self.send_to_client(json.loads(json_str))

    def install(self, name, env, version):
        if env == "none":
            info = subprocess.check_output(
                ["conda", "install", "--json", name])
        else:
            info = subprocess.check_output(
                ["conda", "install", "-n", env, "--json", name])
        json_str = json.dumps(info)
        self.send_to_client(json.loads(json_str))

    def uninstall(self, name, env):
        if env == "none":
            info = subprocess.check_output(
                ["conda", "remove", "--json", name])
        else:
            info = subprocess.check_output(
                ["conda", "remove", "-n", env, "--json", name])
        json_str = json.dumps(info)
        self.send_to_client(json.loads(json_str))

    def send_to_client(self, result):
        # Send `result` to client via Jupyter's Tornado server.
        self.set_header("Content-Type", 'application/json')
        self.write(result)
        self.flush()
        self.finish()
        return
