from setuptools import setup, find_packages, Command
# This runner was created as per
# http://pytest.org/latest/goodpractises.html#integrating-with-distutils-python-setup-py-test
class PyTest(Command):
    user_options = []
    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sys,subprocess
        errno = subprocess.call([sys.executable, 'runtests.py'])
        raise SystemExit(errno)

setup(
    name = "yakirpm",
    version = "0.1",
    author = "rmancy@redhat.com",
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    cmdclass = {'test': PyTest},
    data_files = [('/usr/share/doc/yakirpm', ['README.txt']),]
)
