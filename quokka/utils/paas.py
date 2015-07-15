import os
import sys


def activate():
    # Try OPENSHIFT
    if os.environ.get('OPENSHIFT_HOMEDIR', None):
        sys.path.insert(0, os.path.dirname(__file__) or '.')
        if os.path.exists(os.path.join(
                os.environ['OPENSHIFT_HOMEDIR'], "python-2.6")):
            py_dir = os.path.join(
                os.environ['OPENSHIFT_HOMEDIR'], "python-2.6")
        else:
            py_dir = os.path.join(os.environ['OPENSHIFT_HOMEDIR'], "python")

        virtenv = py_dir + '/virtenv/'
        py_cache = os.path.join(virtenv, 'lib', '2.6', 'site-packages')
        os.environ['PYTHON_EGG_CACHE'] = os.path.join(py_cache)
        virtualenv = os.path.join(virtenv, 'bin/activate_this.py')

        try:
            execfile(virtualenv, dict(__file__=virtualenv))
        except IOError:
            pass
