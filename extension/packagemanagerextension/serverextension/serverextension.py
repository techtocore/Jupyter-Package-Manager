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
        if action == 'pip_list':
            self.pip_list()
            return
        
        result = 'API Status: Live'
        self.send_to_client(result)
        return

    def pip_list(self):
        info = subprocess.check_output(["pip", "list", "--format=json"])
        json_str = json.dumps(info)
        self.send_to_client(json.loads(json_str)) 

    
    def send_to_client(self, result):
        # Send `result` to client via Jupyter's Tornado server.
        self.write(result)
        self.flush()
        self.finish()
        return
