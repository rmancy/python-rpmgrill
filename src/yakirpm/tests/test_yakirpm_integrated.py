import pytest
import pkg_resources
try:
    import json
except ImportError:
    import simplejson as json
from yakirpm import YakiRPM

def _remove_variables(results_json):
    """Removes variables that we know to be not reproducable."""
    # These values will vary between runs, and cannot
    # be used for testing
    del results_json['results']['timestamp']
    for test_results in results_json['tests']:
        del test_results['run_time']

def test_analyze_local(tmpdir):
    """
    Preload the results we expect and then compare them to the output
    from running rpmgrill.
    """
    expected_fh = open(pkg_resources.resource_filename('yakirpm.tests',
                       'rpmgrill-rpmgrill-0.26-1.fc21.json'))
    expected_contents = expected_fh.read()
    expected_json = json.loads(expected_contents)
    _remove_variables(expected_json)

    yaki = YakiRPM(results_dir=tmpdir.dirname)
    output = yaki.analyze_local(pkg_resources.resource_filename(
        'yakirpm.tests', 'rpms'), 'rpmgrill')

    _remove_variables(output)
    assert output == expected_json

def test_list_plugins():
    """
    Test that we return a list of plugins (whatever they may be)
    """
    yaki = YakiRPM()
    plugins = yaki.list_plugins()
    assert isinstance(plugins, dict)
    # i.e, that it is not empty
    assert plugins
