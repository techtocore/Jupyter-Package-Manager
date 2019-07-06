import json
import os

from notebook.base.handlers import (
    APIHandler,
    json_errors,
)
from tornado import web, escape

from .envmanager import EnvManager, package_map
from .processhelper import ProcessHelper
from .swanproject import SwanProject

process_helper = ProcessHelper()


class EnvBaseHandler(APIHandler):
    """
    Maintains a reference to the
    'env_manager' which implements all of the conda functions.
    """
    @property
    def env_manager(self):
        """Return our env_manager instance"""
        return self.settings['env_manager']

# -----------------------------------------------------------------------------
# Project Management APIs
# -----------------------------------------------------------------------------


class ManageProjectsHandler(EnvBaseHandler):

    """
    Handler for `GET /projects` which lists the projects.
    """

    @json_errors
    def get(self):
        self.finish(json.dumps(self.env_manager.list_projects()))

    """
    Handler for `POST /projects` which
    creates the specified environment.
    """

    @json_errors
    def post(self):
        data = escape.json_decode(self.request.body)
        directory = data.get('project')
        directory = process_helper.relativeDir(directory)
        env_type = data.get('env_type', 'python3')
        if env_type not in package_map:
            raise web.HTTPError(400)
        try:
            resp = self.env_manager.create_project(directory, env_type)
        except Exception as e:
            resp = {'error': str(e)}
            
        if 'error' not in resp:
            status = 201  # CREATED

        # catch-all ok
        if 'error' in resp:
            status = 400

        self.set_status(status or 200)
        self.finish(json.dumps(resp))

    """
    Handler for `DELETE /projects` which
    deletes the specified projects.
    """

    @json_errors
    def delete(self):
        data = escape.json_decode(self.request.body)
        try:
            dlist = []
            directory = data.get('project')
            if type(directory) == type(dlist):
                for proj in directory:
                    proj = process_helper.relativeDir(proj)
                    resp = self.env_manager.delete_project(proj)
                    dlist.append(resp)
                resp = {'response': dlist}
            else:
                directory = process_helper.relativeDir(directory)
                resp = self.env_manager.delete_project(directory)
        except Exception as e:
                resp = {'error': str(e)}

        if 'error' not in resp:
            status = 200

        # catch-all ok
        if 'error' in resp:
            status = 400

        self.set_status(status or 200)
        self.finish(json.dumps(resp))


class ProjectInfoHandler(EnvBaseHandler):

    """
    Handler for `GET /project_info` which
    returns the internal name of the environment 
    + all packages required along with their status (if already installed or not?)
    """

    @json_errors
    def get(self):
        directory = self.get_argument('project', "None")
        directory = process_helper.relativeDir(directory)
        if self.request.headers.get('Content-Type') == 'text/plain':
            # export requirements file
            folder = directory[:-1].split('/')[-1]
            self.set_header('Content-Disposition',
                            'attachment; filename="%s"' % (folder + '.txt'))
            try:
                swanproj = SwanProject(directory)
                self.write(swanproj.export_env())
            except Exception as e:
                self.write(str(e))
                self.set_status(400)
            # TODO Find why the content-type header is not properly set
            self.set_header('Content-Type', 'text/plain; charset="utf-8"')
            self.finish()
        else:
            # send list of all packages
            try:
                swanproj = SwanProject(directory)
                resp = swanproj.project_info()
            except Exception as e:
                resp = {'error': str(e)}

            if 'error' not in resp:
                status = 200  # OK

            # catch-all ok
            if 'error' in resp:
                status = 400

            self.set_status(status or 200)
            self.finish(json.dumps(resp))

    """
    Handler for `PUT /project_info` which
    updates a project with all the packages obtained from an export file
    """

    @json_errors
    def put(self):
        # get list of all packages
        file1 = self.request.files['file'][0]
        directory = self.get_argument('project', default=None)
        directory = process_helper.relativeDir(directory)
        tmp = file1['body'].splitlines()
        packages = []
        for i in tmp:
            if i[0] != '#':
                packages.append(i)

        try:
            swanproj = SwanProject(directory)
            resp = swanproj.install_packages(packages)
        except Exception as e:
            resp = {'error': str(e)}

        if 'error' not in resp:
            status = 200  # OK

        # catch-all ok
        if 'error' in resp:
            status = 400

        self.set_status(status or 200)
        self.finish(json.dumps(resp))

    """
    Handler for `PATCH /project_info` which
    syncs a .swanproject file and the corresponding conda env
    """

    @json_errors
    def patch(self):
        data = escape.json_decode(self.request.body)
        directory = data.get('project')
        directory = process_helper.relativeDir(directory)
        try:
            swanproj = SwanProject(directory)
            resp = swanproj.sync_packages()
        except Exception as e:
            resp = {'error': str(e)}

        if 'error' not in resp:
            status = 200  # OK

        # catch-all ok
        if 'error' in resp:
            status = 400

        self.set_status(status or 200)
        self.finish(json.dumps(resp))
