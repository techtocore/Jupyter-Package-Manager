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

MAX_LOG_OUTPUT = 6000

CONDA_EXE = os.environ.get("CONDA_EXE", "conda")  # type: str

# try to match lines of json
JSONISH_RE = r'(^\s*["\{\}\[\],\d])|(["\}\}\[\],\d]\s*$)'


class ProcessHelper(LoggingConfigurable):

    @classmethod
    def pkg_info(self, s):
        return {
            "build_string": s.get("build_string", s.get("build")),
            "name": s.get("name"),
            "version": s.get("version")
        }

    @classmethod
    def pkg_info_status(self, s, names):
        pkg_info_res = self.pkg_info(s)
        name = pkg_info_res.get("name")
        status = "not available"
        if name in names:
            status = "installed"
        pkg_info_res['status'] = status
        return pkg_info_res

    @classmethod
    def conda_execute(self, cmd, *args):
        cmd = CONDA_EXE + ' ' + cmd
        cmdline = cmd.split() + list(args)

        try:
            output = check_output(cmdline)
        except CalledProcessError as exc:
            output = exc.output

        return output.decode("utf-8")

    @classmethod
    def clean_conda_json(self, output):
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
