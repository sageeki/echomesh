from __future__ import absolute_import, division, print_function, unicode_literals

import os
import os.path
import time

from echomesh.base import CommandFile
from echomesh.base import Path
from echomesh.util import Flag
from echomesh.util import Log
from echomesh.util import Scope
from echomesh.util import SizeName

LOGGER = Log.logger(__name__)

def _time(t):
  return time.strftime('%H:%M', time.localtime(t))

ELEMENT_FORMAT = '%-28s %5s %9s %9s %9s'

def scopes(echomesh):
  LOGGER.print('  ' + ('\n  '.join(CommandFile.COMMAND_PATH)))

SCOPES_HELP = """
In order to control multiple machines and configurations effectively, echomesh
configurations and scores live in one of five different types of "scopes".

4.global:
  This is the global scope that comes with echomesh and contains only the
  default configuration, which cannot be changed by echomesh programs.

3.platform:
  The platform scope contains scores that are specific to platform of the
  machine that echomesh is running on, i.e the operating system and hardware.

  Right now, we have three platforms:  linux, darwin and windows.

2.tag:
  At configuration time, you can specify text tags for each machine.

1.name:
  This directory contains scores that are only associated with a machine with
  the given name.

0.local:
  These are temporary, local files that aren't stored anywhere else.  They're
  used to make changes for experimentation.

"""


def _scores(path, resolve=False, scope='all', recursive=False):
  printed = False
  if scope == 'all':
    for s in Scope.SCOPES:
      printed = _scores(path, resolve, s, recursive) or printed
  else:
    scope = Scope.resolve(scope)
    pathdir = os.path.join(Path.COMMAND_PATH, scope, 'score', path)
    if os.path.isdir(pathdir):
      printed_this_time = False
      for f in sorted(os.listdir(pathdir)):
        joined_f = os.path.join(pathdir, f)
        is_dir = os.path.isdir(joined_f)
        if not (is_dir or f.endswith('yml')):
          continue
        if not printed_this_time:
          printed_this_time = True
          if not printed:
            LOGGER.print(ELEMENT_FORMAT, 'File name', 'Size', 'Accessed',
                         'Modified', 'Created')
            printed = True
          else:
            LOGGER.print('\n')
          LOGGER.print('  %s/%s:', scope, path)
        if is_dir:
          LOGGER.print('    %s/', f)
        else:
          stat = os.stat(joined_f)
          LOGGER.print(ELEMENT_FORMAT,
                       '    ' + f, SizeName.size_name(stat.st_size),
                       _time(stat.st_atime),
                       _time(stat.st_mtime),
                       _time(stat.st_ctime))
  return printed

SCORES_HELP = """
"show scores" shows some or all of the scores in the echomesh project.

Because of the resolution of score names, there are multiple areas where scores
might be found, called "scopes".

If you just type "show scores" you'll see all in the top directory.
If you want to see items in a subdirecto

The full form of the command is

  show scores

See "help show scopes" for more information.
"""

def scores(echomesh, *args):
  flags, paths = Flag.split_args(args)
  paths = paths or ['']
  for p in paths:
    _scores(p, **flags)