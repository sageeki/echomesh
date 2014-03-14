from __future__ import absolute_import, division, print_function, unicode_literals

import cechomesh

from echomesh.pattern.Pattern import Pattern

class Fade(Pattern):
  SETTINGS = {
    'fade': {
      'default': 0.0,
      'help': '',
      },
    'smooth': {
      'default': 0,
      'help': '',
      },
    }

  def _evaluate(self):
    patterns = self.patterns()
    if not patterns:
      return []
    steps = len(patterns) - 1
    if not steps:
      return patterns[0]

    fade_value = self.get('fade')
    total_fade = fade_value * steps
    segment = int(total_fade)
    fade = total_fade - segment
    if segment < steps:
      return cechomesh.to_color_list(patterns[segment]).interpolate(
        patterns[segment + 1], fade, self.get('smooth'))
    else:
      return patterns[segment]
