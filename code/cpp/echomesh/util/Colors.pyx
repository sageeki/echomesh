from libcpp.string cimport string

cdef extern from "echomesh/util/Colors.h" namespace "echomesh":
  cdef cppclass FColor:
    float red_
    float green_
    float blue_
    float alpha_

cdef extern from "echomesh/util/Colors.h" namespace "echomesh::FColor":
  FColor NO_COLOR

ctypedef vector[FColor] FColorList

cdef extern from "echomesh/util/Colors.h" namespace "echomesh":
  bool fillColor(string name, FColor* color)
  FColor colorFromInt(unsigned int argb)
  void copyColor(FColor c1, FColor* c2)
  string colorName(FColor color)
  void sortFColorList(FColorList*)
  int compareColors(FColor x, FColor y)
  int countColorsInList(FColorList, FColor)
  int indexColorInList(FColorList, FColor)
  void reverseFColorList(FColorList*)
  void fillFColorList(FColorList*, FColor begin, FColor end, int size)
  FColor interpolate(FColor begin, FColor end, int index, int size)
  FColor makeFColor(float red, float green, float blue, float alpha)

