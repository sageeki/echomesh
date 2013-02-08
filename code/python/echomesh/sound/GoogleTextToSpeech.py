from __future__ import absolute_import, division, print_function, unicode_literals

import copy
import requests

from echomesh.util.file import Cache

URL = 'http://translate.google.com/translate_tts'
HEADERS = {'User-Agent': 'Mozilla'}
PARAMS = {'ie': 'UTF-8'}

def text_to_speech(text, tl='en'):
  """
  Given a phrase in a language that Google translate supports, returns a binary
  string representing an mp3 file, or raises an exception if this is impossible.

  """
  params = dict(PARAMS, q=text, tl=tl)
  r = requests.get(URL, params=params, headers=headers)
  if not r.ok:
    raise Exception("%d: couldn't read URL %s for '%s'" %
                    (r.status_code, r.url, text))
  return r.content

class TextToSpeechCache(Cache.Cache):
  INSTANCE = None

  @classmethod
  def instance(cls):
    if not cls.INSTANCE:
      cls.INSTANCE = TextToSpeechCache(name='text-to-speech')

  def _get_file_contents(self, key):
    return text_to_speech(key)
