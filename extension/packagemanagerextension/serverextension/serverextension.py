from notebook.base.handlers import IPythonHandler
import sys
import os

# For now write logs in ~/packgeManager-monitoring.txt
sys.stdout = open(os.path.join(os.path.expanduser('~'),
                               'packgeManager-monitoring.txt'), 'w')


class PackageManagerHandler(IPythonHandler):

    def get(self):
        """
        This method handles all the `GET` requests recieved on the server extension. 
        """
        result = 'test1'
        self.send_to_client(result)
        return

    def send_to_client(self, result):
        # Send `result` to client via Jupyter's Tornado server.
        self.write(result)
        self.flush()
        self.finish()
        return
