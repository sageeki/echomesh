from __future__ import absolute_import, division, print_function, unicode_literals

from echomesh.util import Subprocess

if __name__ == '__main__':
  for line in Subprocess.run(['sudo', 'ls', '/root'])[1].splitlines():
    print(line)
