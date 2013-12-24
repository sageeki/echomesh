from libcpp.vector cimport vector

cdef eraseColourList(ColourList* cl, int x, int y):
  cl.erase(cl.begin() + x, cl.begin() + y)

cdef insertColourList(ColourList frm, int s1, int s2, ColourList* to, int t):
  to.insert(to.begin() + 1, frm.begin() + s1, frm.begin() + s2)

cdef setColourInList(ColourList* cl, int pos, Colour c):
  copyColor(c, &cl.at(pos))

cdef eraseInList(ColourList* cl, int pos):
  cl.erase(cl.begin() + pos)

def _make_list(object value):
  try:
    len(value)
  except:
    value = list(value)
  return value

cdef class ColorList:
  cdef ColourList* thisptr

  def __cinit__(self, *args):
    self.thisptr = new ColourList()
    if len(args) == 1:
      self.extend(args[0])
    elif args:
      raise TypeError('ColorList takes at most 1 argument (%d given)' % len(args))

  def __dealloc__(self):
    del self.thisptr

  def append(self, object item):
    cdef Colour c
    if fill_colour(item, &c):
      self.thisptr.push_back(c)
    else:
      raise ValueError('Don\'t understand color value %s' % item)

  def count(self, object item):
    cdef Colour c
    if not fill_colour(item, &c):
      raise ValueError('Don\'t understand color value %s' % item)
    return countColorsInList(self.thisptr[0], c)

  def extend(self, object items):
    length = len(self)
    items = _make_list(items)
    new_length = len(items)

    self.thisptr.reserve(length + new_length)
    try:
      for item in items:
        self.append(item)
    except:
      self.thisptr.resize(length)

  def index(self, object item):
    cdef Colour c
    if not fill_colour(item, &c):
      raise ValueError('Don\'t understand color value %s' % item)
    index = indexColorInList(self.thisptr[0], c)
    if index >= 0:
      return index
    raise ValueError('%s is not in ColorList' % item)

  def insert(self, int index, object item):
    self[index:index] = [item]

  def pop(self, int index=-1):
    index = self._check_key(index)
    item = self[index]
    del self[index]
    return item

  def remove(self, object item):
    del self[self.index(item)]

  def reverse(self):
    reverseColorList(self.thisptr)

  def sort(self):
    sortColorList(self.thisptr)

  def __add__(self, object other):
    cl = ColorList(self)
    cl.extend(other)
    return cl

  def __contains__(self, object item):
    try:
      self.index(item)
      return True
    except ValueError:
      return False

  def __delitem__(self, key):
    eraseInList(self.thisptr, self._check_key(key))

  def __getitem__(self, object key):
    if isinstance(key, slice):
      start, stop, stride = slice.indices(len(self))
      size = (stop - start) / stride
      cl = ColorList(size)
      i = 0
      while start < stop:
        copyColor(self.thisptr.at(start), &cl.thisptr.at(i))
        start += stride
        i += 1
      return cl

    else:
      key = self._check_key(key)
      color = Color()
      color.thisptr[0] = self.thisptr.at(key)
      return color

  def __imul__(self, object other):
    pass

  def __len__(self):
    return self.thisptr.size()

  def __iadd__(self, object other):
    pass

  def __mul__(self, object other):
    pass

  def __radd__(self, object other):
    pass

  def __repr__(self):
    return 'ColorList(%s)' % self.__str__()

  def __reversed__(self):
    pass

  def __rmul__(self, object other):
    pass

  def __setitem__(self, object key, object value):
    if isinstance(key, slice):
      value = _make_list(value)
      if isinstance(value, ColorList):
        cl = <ColorList> value
      else:
        cl = ColorList(value)

      length = len(cl)
      start, stop, stride = key.indices(len(self))
      slice_length = int((stop - start) / stride)

      if slice_length != length:
        if stride != 1:
          raise ValueError('attempt to assign sequence of size %s '
                           'to extended slice of size %d' %
                           (length, slice_length))

        if slice_length > length:
          eraseColourList(self.thisptr, length, slice_length)
        else:
          insertColourList(cl.thisptr[0], slice_length, length, self.thisptr,
                           start + slice_length)

      for i in range(length):
        assert start < stop
        copyColor(cl.thisptr.at(i), &self.thisptr.at(start))
        start += stride

    else:
      key = self._check_key(key)
      if not fill_colour(value, &self.thisptr.at(key)):
        raise ValueError('Don\'t understand color value %s' % value)

  def __sizeof__(self):
    pass

  def __str__(self):
    return '[%s]' % ', '.join(str(c) for c in self)

  def _check_key(self, int key):
    if key >= 0:
      if key < len(self):
        return key
    else:
      if -key <= len(self):
        return len(self) + key
    raise IndexError('ColorList index out of range')

  def _set_item(self, int i, object item):
    cdef Colour c
    if fill_colour(item, &c):
      setColourInList(self.thisptr, i, c)
    else:
      raise ValueError('Don\'t understand color value %s' % item)

