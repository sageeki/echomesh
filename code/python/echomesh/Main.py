from __future__ import absolute_import, division, print_function, unicode_literals

USE_DIGITS_FOR_PROGRESS_BAR = False
COUNT = 0

def _main():
  import sys

  times = []

  def p(msg=''):
    """Print progress messages while echomesh loads."""
    print(msg, end='\n' if msg else '')
    global COUNT
    dot = str(COUNT % 10) if USE_DIGITS_FOR_PROGRESS_BAR else '.'
    print(dot, end='')
    COUNT += 1

    sys.stdout.flush()

    import time
    times.append(time.time())

  p('Loading echomesh ')

  from echomesh.base import Version
  if Version.TOO_NEW:
    print(Version.ERROR)

  from echomesh.base import Path
  if not Path.PROJECT_PATH:
    return
  p()


  Path.fix_sys_path()
  p()

  from echomesh.base import Args
  p()

  if not Args.set_arguments(sys.argv):
    return

  p()

  from echomesh.base import Config
  p()

  Config.recalculate()
  p()

  if Config.get('autostart') and not Config.get('permission', 'autostart'):
    print()
    from echomesh.util import Log
    Log.logger(__name__).info("Not autostarting because autostart=False")
    return

  p()

  from echomesh import Instance
  print()

  if Config.get('diagnostics', 'startup_times'):
    print()
    for i in range(len(times) - 1):
      print(i, ':', int(1000 * (times[i + 1] - times[i])))
    print()

  Instance.main()

  if Config.get('diagnostics', 'unused_configs'):
    import yaml
    print(yaml.safe_dump(Config.get_unvisited()))

def main():
  try:
    _main()
  except:
    import traceback
    print(traceback.format_exc())

