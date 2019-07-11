import json

from notebook.base.handlers import (
    APIHandler,
    json_errors,
)
from tornado import web, escape

from .packagemanagement import PackageManager, CondaSearcher

package_manager = PackageManager()

'''
This file contains the handler classes for API endpoints. Every request is serviced by calling
an appropriate method from the PackageManager class
'''


class EnvBaseHandler(APIHandler):

    '''
    Maintains a reference to the
    'env_manager' which implements all of the conda functions.
    '''

    @property
    def env_manager(self):
        '''
        Return our env_manager instance
        '''
        return self.settings['env_manager']


# -----------------------------------------------------------------------------
# Project Management APIs
# -----------------------------------------------------------------------------


class ManageProjectsHandler(EnvBaseHandler):

    @json_errors
    def get(self):
        '''
        Handler for `GET /projects` which lists the projects.
        '''

        resp = {}
        resp['projects'] = package_manager.list_projects()
        self.finish(json.dumps(resp))

    @json_errors
    def post(self):
        '''
        Handler for `POST /projects` which
        creates the specified environment.
        '''

        data = escape.json_decode(self.request.body)
        directory = data.get('project')
        env_type = data.get('env_type', 'python3')
        resp = package_manager.create_project(directory, env_type)

        if 'error' not in resp:
            status = 201  # CREATED

        # catch-all ok
        if 'error' in resp:
            status = 400

        self.set_status(status or 200)
        self.finish(json.dumps(resp))

    @json_errors
    def delete(self):
        '''
        Handler for `DELETE /projects` which
        deletes the specified projects.
        '''

        data = escape.json_decode(self.request.body)
        directories = data.get('project')
        resp = package_manager.delete_project(directories)

        if 'error' not in resp:
            status = 200

        # catch-all ok
        if 'error' in resp:
            status = 400

        self.set_status(status or 200)
        self.finish(json.dumps(resp))


class ProjectInfoHandler(EnvBaseHandler):

    @json_errors
    def get(self):
        '''
        Handler for `GET /project_info` which
        returns the internal name of the environment 
        + all packages required along with their status (if already installed or not?)
        '''

        directory = self.get_argument('project', "None")
        if self.request.headers.get('Content-Type') == 'text/plain':
            # export requirements file
            folder = directory[:-1].split('/')[-1]
            self.set_header('Content-Type', 'text/plain; charset="utf-8"')
            self.set_header('Content-Disposition',
                            'attachment; filename="%s"' % (folder + '.txt'))
            self.write(package_manager.export_package_text(directory))
            self.finish()
        else:
            # send list of all packages
            resp = package_manager.project_info(directory)

            if 'error' not in resp:
                status = 200  # OK

            # catch-all ok
            if 'error' in resp:
                status = 400

            self.set_status(status or 200)
            self.finish(json.dumps(resp))

    @json_errors
    def put(self):
        '''
        Handler for `PUT /project_info` which
        updates a project with all the packages obtained from an export file
        '''

        # get list of all packages
        file1 = self.request.files['file'][0]
        directory = self.get_argument('project', default=None)

        resp = package_manager.import_project(file1, directory)

        if 'error' not in resp:
            status = 200  # OK

        # catch-all ok
        if 'error' in resp:
            status = 400

        self.set_status(status or 200)
        self.finish(json.dumps(resp))

    @json_errors
    def patch(self):
        '''
        Handler for `PATCH /project_info` which
        syncs a .swanproject file and the corresponding conda env
        '''

        data = escape.json_decode(self.request.body)
        directory = data.get('project')

        resp = package_manager.sync_project(directory)

        if 'error' not in resp:
            status = 200  # OK

        # catch-all ok
        if 'error' in resp:
            status = 400

        self.set_status(status or 200)
        self.finish(json.dumps(resp))


# -----------------------------------------------------------------------------
# Package Management APIs
# -----------------------------------------------------------------------------


class PkgHandler(EnvBaseHandler):

    @json_errors
    def post(self):
        '''
        Handler for `POST /packages` which installs all
        the selected packages in the specified environment.
        '''

        data = escape.json_decode(self.request.body)
        directory = data.get('project')
        packages = data.get('packages')
        resp = package_manager.install_packages(directory, packages)
        if resp.get("error"):
            self.set_status(400)
        self.finish(json.dumps(resp))

    @json_errors
    def patch(self):
        '''
        Handler for `PATCH /packages` which updates all
        the selected packages in the specified environment.
        '''

        data = escape.json_decode(self.request.body)
        directory = data.get('project')
        packages = data.get('packages')
        resp = package_manager.update_packages(directory, packages)
        if resp.get("error"):
            self.set_status(400)
        self.finish(json.dumps(resp))

    @json_errors
    def delete(self):
        '''
        Handler for `DELETE /packages` which deletes all
        the selected packages in the specified environment.
        '''

        data = escape.json_decode(self.request.body)
        directory = data.get('project')
        packages = data.get('packages')
        resp = package_manager.delete_packages(directory, packages)
        if resp.get("error"):
            self.set_status(400)
        self.finish(json.dumps(resp))


class CheckUpdatePkgHandler(EnvBaseHandler):

    @json_errors
    def get(self):
        '''
        Handler for `GET /packages/check_update` which checks for updates of all
        the selected packages in the specified environment.
        '''

        directory = self.get_argument('project', "None")
        resp = package_manager.check_update(directory)
        if resp.get("error"):
            self.set_status(400)
        self.finish(json.dumps(resp))


class CloneProjectHandler(EnvBaseHandler):

    @json_errors
    def post(self):
        '''
        Handler for for `POST /project_clone` which clones a project in a new location
        '''

        data = escape.json_decode(self.request.body)
        directory = data.get('project')
        resp = package_manager.clone_project(directory)
        if resp.get("error"):
            self.set_status(400)
        self.finish(json.dumps(resp))


searcher = CondaSearcher()


class AvailablePackagesHandler(EnvBaseHandler):

    @json_errors
    def get(self):
        '''
        Handler for `GET /packages/available`, which uses CondaSearcher
        to list the packages available for installation.
        '''

        data = searcher.list_available(self)

        if data is None:
            # tell client to check back later
            self.clear()
            self.set_status(202)  # Accepted
            self.finish('{}')
        else:
            self.finish(json.dumps({"packages": data}))


class SearchHandler(EnvBaseHandler):

    @json_errors
    def get(self):
        '''
        Handler for `GET /packages/search?q=<query>`, which uses CondaSearcher
        to search the available conda packages.
        '''

        q = self.get_argument('q', "None")
        resp = {}
        resp['packages'] = package_manager.search(q)
        self.finish(json.dumps(resp))
