from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import getpass
import os
import sys
import yaml

from os.path import abspath, dirname

import yaml

from echomesh.base import CommandFile
from echomesh.base import File
from echomesh.base import Merge
from echomesh.base import Platform

CONFIG = None
CONFIGS_UNVISITED = None  # Report on config items that aren't used.
CODE_PATH = None
NAME = None

def _add_exception_suffix(e, suffix):
  e.args = tuple(a + suffix for a in e.args)

def _merge_level_files():
  # Load merged configuration file from the command directory hierarchy.
  config = None
  for f in reversed(CommandFile.expand('config.yml')):
    try:
      cfg = File.yaml_load(f)
    except:
      raise Exception('Error in configuration file %s' % f)

    if config is None:
      config = cfg
    else:
      try:
        Merge.merge(config, cfg)
      except Exception as e:
        _add_exception_suffix(e, ' in configuration file %s' % f)
        raise
  return config

def _merge_command_line_arguments(args, config):
  for i, arg in enumerate(args):
    if i:
      try:
        cfgs = File.yaml_load_stream(arg)
      except:
        raise Exception('Error in command line argument %d: "%s"' % (i, arg))

      try:
        Merge.merge_all(config, *cfgs)
      except Exception as e:
        _add_exception_suffix(e, ' in command line argument %d: "%s"' % (i, arg))
        raise
  return config

def recalculate(*args):
  global CONFIG, CONFIGS_UNVISITED, CODE_PATH
  if not CONFIG:
    # If running as root, export user pi's home directory as $HOME.
    if getpass.getuser() == 'root':
      os.environ['HOME'] = '/home/pi'

    CODE_PATH = sys.path[0]

    local_path = ''
    if len(sys.argv) > 1:
      arg = sys.argv[1]
      if not arg[0] in '{[':
        os.chdir(arg)

    CONFIG = _merge_command_line_arguments(args, _merge_level_files())
    CONFIGS_UNVISITED = copy.deepcopy(CONFIG)

def is_control_program():
  """is_control_program() is True if Echomesh responds to keyboard commands."""
  return get('control_program', 'enable')

def get(*parts):
  recalculate()

  config, unvisited = CONFIG, CONFIGS_UNVISITED
  def get_part(config, part):
    if not isinstance(config, dict):
      raise Exception("Reached leaf configuration for %s" % ':'.join(parts))
    value = config.get(part, None)
    if value is None:
      raise Exception("Couldn't find configuration %s" % ':'.join(parts))
    return value

  for part in parts[:-1]:
    config = get_part(config, part)
    if unvisited:
      unvisited = unvisited.get(part, None)

  last_part = parts[-1]
  value = get_part(config, last_part)

  if isinstance(value, dict):
    raise Exception("Didn't reach leaf configuration for %s" % ':'.join(parts))

  del unvisited[last_part]
  return value

def get_unvisited():
  def fix(d):
    if isinstance(d, dict):
      for k, v in list(d.iteritems()):
        assert v is not None
        fix(v)
        if v == {}:
          del d[k]
    return d
  if not True:
    return CONFIGS_UNVISITED
  return fix(copy.deepcopy(CONFIGS_UNVISITED))


# The following code is all deprecated.
# TODO: find a better way to broadcast persistent changes to all the nodes.

def change(config):
  File.yaml_dump_all(LOCAL_CHANGED_FILE, config)
  Merge.merge_into(CONFIG, File.yaml_load(sys.argv[1]))


# TODO: a "clear" command that undoes the "change" command.  A tiny bit tricky,
# because we'd have to revert the main config to its original value "in place".

def remove_local():
  os.remove(_config_file('local'))
  global CONFIG
  CONFIG = recalculate()
