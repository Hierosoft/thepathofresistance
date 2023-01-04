# -*- coding: utf-8 -*-
'''

pull_images
-----------

This script moves images that the SLA file cites from a different
directory where it has no missing image errors to the current directory,
to fix current missing image errors.

Usage:
pull_images <SLA file> <old directory>

'''
from __future__ import print_function
from __future__ import division
import sys
import os

if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# from tabletopper.find_pyscribus import pyscribus
# import pyscribus.sla as sla
from tabletopper.find_hierosoft import hierosoft

from hierosoft import (
    echo0,
    echo1,
    echo2,
    replace_vars,
    # set_verbosity,
    # get_verbosity,
)

from hierosoft.simpleargs import (
    SimpleArgs,
)

from hierosoft.moreweb import (
    HTMLParser,  # debug only (for testing hierosoft issue #3)
)

from tabletopper.morescribus import (
    ScribusProject,
)

makedir_logged_lines = set()


def move_safe(src, dst):
    parent_dir = os.path.dirname(dst)
    if not os.path.isdir(parent_dir):
        msg = 'mkdir -p "{}"'.format(parent_dir)
        if msg not in makedir_logged_lines:
            makedir_logged_lines.add(msg)
            print(msg)
        # os.makedirs(parent_dir)
    print('mv "{}" "{}"'.format(src, dst))
    # shutil.move(src, dst)


'''
def pull_images(options):
    echo0("options={}".format(options))
    old_dir = options['old_dir']
    sla_file = options['sla_file']

    parsed = sla.SLA(sla_file, "1.5.8")
    # ^ fails with "pyscribus.exceptions.InvalidDim: Pica points must
    #   not be inferior to 0." See
    #   <https://framagit.org/etnadji/pyscribus/-/issues/1>
    #   (See also unrelated
    #   <http://etnadji.fr/pyscribus/guide/en/psm.html>)

    return 0
'''

ERROR_MISSING_ARG = 1
ERROR_BAD_PATH = 2


def pull_images(DST_FILE, OLD_DIR):
    DST_FILE = sys.argv[1]
    OLD_DIR = sys.argv[2]
    # EXAMPLE_OUT_FILE = os.path.splitext(DST_FILE)[0] + ".example-output.sla"
    if not os.path.isfile(DST_FILE):
        echo('Error: "{}" does not exist.')
        return ERROR_BAD_PATH
    # set_verbosity(1)
    # echo0('The module will run in the example with verbosity={}.'
    #       ''.format(get_verbosity()))
    if not os.path.isdir(OLD_DIR):
        '''
        echo0('There is no "{}" for checking the move feature, so '
              ' missing files will be checked using relative paths'
              ' (OK if already ready for Scribus,'
              ' since it uses relative paths).')
        '''
        echo0('Error: OLD_DIR "{}" does not exist.'.format(OLD_DIR))
        return ERROR_BAD_PATH
        OLD_DIR = os.path.dirname(DST_FILE)
    else:
        echo0('Looking for missing files to move from "{}" for "{}"'
              ''.format(OLD_DIR, os.path.split(DST_FILE)[1]))

    project = ScribusProject(DST_FILE)
    project.move_images(OLD_DIR)
    # project.save()
    # echo0('Done writing "{}"'.format(project.get_path()))
    return 0


def main():
    """
    See The module docstring for help.
    """

    '''
    if len(sys.argv) < 3:
        echo0()
        echo0()
        echo0(__doc__)
        echo0("Error: You must specify the old directory"
              " where the SLA was before moving it.")
        return 1
    sequential_keys = ['sla_file', 'old_dir']
    simpleargs = SimpleArgs(None,
        sequential_keys=sequential_keys,
        required=sequential_keys,
        # flags = ['--pyscribus'],
        usage_docstring=__doc__,
    )
    try:
        simpleargs.collect()
    except Exception as ex:
        simpleargs.usage()
        echo0("Error: {}".format(ex))
        return 1

    return pull_images(simpleargs.options)
    '''

    # MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
    # REPO_DIR = os.path.dirname(MODULE_DIR)
    EXAMPLE_FILE = os.path.join(REPO_DIR, "The Path of Resistance.sla")
    OLD_DIR = os.path.join(replace_vars("%CLOUD%"), "Tabletop", "Campaigns",
                           "The Path of Resistance")
    if len(sys.argv) != 3:
        echo0("Error: You must specify the new file and the old directory"
              " to gather files used by the file.")
        if os.path.isdir(OLD_DIR):
            echo0("Such as:")
            echo0('pull_images "{}" "{}"'.format(EXAMPLE_FILE, OLD_DIR))
        return 1
    # DST_FILE = EXAMPLE_FILE
    return pull_images(sys.argv[1], sys.argv[2])


if __name__ == "__main__":
    sys.exit(main())
