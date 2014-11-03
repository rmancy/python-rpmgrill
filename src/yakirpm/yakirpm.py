import os
import re
try:
    import json
except ImportError:
    import simplejson as json
from glob import glob
from subprocess import Popen, PIPE


class YakiRPM(object):
    """YakiRPM does local analysis via rpmgrill."""

    # All rpmgrill's result files are suffixed with this
    _result_file_suffix = 'rpmgrill-'
    _analyze_command = '/usr/bin/rpmgrill-analyze-local'
    _rpmgrill_command = '/usr/bin/rpmgrill'

    @classmethod
    def _run_rpmgrill(cls, command):
        """Run our rpmgrill command."""
        p = Popen(command, stderr=PIPE, stdout=PIPE)
        rpmgrill_stdout, rpmgrill_stderr = p.communicate()
        if p.returncode != 0:
            raise RuntimeError('Rpmgrill failed with returncode %s.'
                'Error was: %s' % (p.returncode, rpmgrill_stderr))
        return rpmgrill_stdout

    @classmethod
    def _verify_list_plugins_output(cls, stdout_lines):
        """
        Make sure we have expected the leading output from rpmgrill.
        """
        assert stdout_lines[0] == ('Available rpmgrill plugins, in the order'
            ' in which they run:')
        assert stdout_lines[1] == ''

    @classmethod
    def _encode_results(cls, result_file):
        """ Encode our results in our result file into a JSON object."""
        result_fh = open(result_file)
        result_contents = result_fh.read()
        return json.loads(result_contents)

    def __init__(self, results_dir=None):
        self.build_log = 'build.log'
        self.results_dir = results_dir or os.getcwd()

    def _plugin_description_to_dict(self, list_plugins_output):
        """ Convert rpmgrills plugins output to a dict."""
        # Later versions of rpmgrill may break us, so let's make sure
        # we know what output we are dealing with
        self._verify_list_plugins_output(list_plugins_output)
        plugins_and_descriptions = list_plugins_output[2:]
        plugins = {}
        for plugin_and_description in plugins_and_descriptions:
            m = re.search('^\s+(.+?)\s+(.+?)$', plugin_and_description)
            try:
                plugin = m.group(1)
                description = m.group(2)
            except AttributeError:
                raise RuntimeError("Rpmgrill's plugin output was unexpected:"
                    " %s" % list_plugins_output)
            plugins[plugin.strip()] = description.strip()

        return plugins

    def list_plugins(self):
        """List all the plugins(tests) that rpmgrill can run."""
        _stdout = self._run_rpmgrill([self._rpmgrill_command, '--list-plugins'])
        stdout_lines = _stdout.splitlines()
        # It just so happens that plugins are perl modules
        # so there are no spaces in their name. We use this to determine
        return self._plugin_description_to_dict(stdout_lines)

    def analyze_local(self, rpm_dir, rpm_nvr):
        """ Analyze local RPMs via rpmgrill.

        Creates a glob from rpm_dir and rpm_nvr and analyses all RPMs
        matched by the glob. Note that a src RPM needs to be present,
        and rpmgrill expects all rpms to be of the same nvr
        """
        cmd_args = [self._analyze_command]
        rpm_glob_pattern = os.path.join(rpm_dir, '%s*.rpm' % rpm_nvr)
        files_found = glob(rpm_glob_pattern)
        if not files_found:
            raise RuntimeError('No files found with glob pattern: %s' %
                rpm_glob_pattern)
        cmd_args += files_found
        build_log_location = os.path.join(rpm_dir, self.build_log)
        if os.path.exists(build_log_location):
            cmd_args.append(build_log_location)
        cmd_args += ['--results-dir', self.results_dir]
        # This will invoke rpmgrill-analyze-local which will
        # write result files to disk.
        self._run_rpmgrill(cmd_args)
        return self._read_results(rpm_nvr)

    def _read_results(self, rpm_nvr):
        """Read in the results file created by rpmgrill."""
        result_files = [file_ for file_
                        in glob(os.path.join(self.results_dir, '%s%s*' %
                        (self._result_file_suffix, rpm_nvr)))
                        if file_.endswith('json')]
        # rpmgrill currently only deals with one build result at a time,
        # so we're assuming only one JSON result file, but let's assert it
        assert len(result_files) == 1, ('Rpmgrill gave more result files than'
            ' expected')
        return self._encode_results(result_files[0])

