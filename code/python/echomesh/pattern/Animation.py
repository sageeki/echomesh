from __future__ import absolute_import, division, print_function, unicode_literals

import PIL
from echomesh.Cechomesh import cechomesh

from echomesh.pattern.Image import Image
from echomesh.pattern import Pattern
from echomesh.util import Log
from echomesh.util.image import Resize
from echomesh.util.image.MakeImage import make_image

LOGGER = Log.logger(__name__)

class Animation(Image):
    HELP = """Displays a GIF animation.  You can control the playback
  with the "frame" setting."""

    SETTINGS = Pattern.copy_const_settings(
      Image,
      frame={
        'default': 0.0,
        'help': ('Controls which frame from the animation is being displayed.'
                 'frame=0.0 displays the first frame, frame=1.0 displays the '
                 'last frame, and a value between 0 and 1 displays one of the '
                 'intermediate frames.'),
        },
      smooth={
        'default': False,
        'help': 'If true, then Animation interpolates between frames.',
        },
      )

    def _precompute(self):
        self.cells = []
        image = self._get_image()
        if not image:
            raise Exception('No image %s' % filename)
        while True:
            self.cells.append(self._image_to_list(image))
            try:
                image.seek(image.tell() + 1)
            except EOFError:
                break
        self.length = 1 + len(self.cells)
        # +1 because we need a full cell between the end cell and the start.

    def _evaluate(self):
        frame = ((self.get('frame') / self.length) % 1) * self.length
        floor = min(int(frame), len(self.cells) - 1)
        if floor == frame or not self.get('smooth'):
            return self.cells[floor]
        ceil = floor + 1
        if ceil >= len(self.cells):
            ceil = 0

        return self.cells[floor].interpolate(
            self.cells[ceil], frame - floor, False)
