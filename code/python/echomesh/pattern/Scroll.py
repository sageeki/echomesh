from __future__ import absolute_import, division, print_function, unicode_literals

import cechomesh

from echomesh.base import Config
from echomesh.pattern.Pattern import Pattern

class Scroll(Pattern):
  SETTINGS = {
    'columns': {
      'default': None,
      'help': '',
      },
    'dx': {
      'default': 0,
      'help': '',
      },
    'dy': {
      'default': 0,
      'help': '',
      },
    'smooth': {
      'default': True,
      'help': '',
      },
    'transform': {
      'default': '',
      'help': '',
      },
    'wrap': {
      'default': False,
      'help': '',
      },
    }
  PATTERN_COUNT = 1

  def _evaluate(self):
    color_list = self.patterns()[0]

    columns = (self.get('columns') or
               getattr(color_list, 'columns', 0) or
               Config.get('light', 'visualizer', 'layout')[0])

    return cechomesh.scroll_color_list(
      color_list, self.get('dx'), self.get('dy'), columns=columns,
      wrap=self.get('wrap'), smooth=self.get('smooth'),
      transform=self.get('transform'))