cdef extern from "echomesh/color/FColorList.h" namespace "echomesh::color":
  cdef cppclass FColorList:
    FColor& at(int pos)
    void combine(FColorList)
    void copy(FColorList)
    int count(FColor)
    void extend(FColorList)
    void eraseOne(int pos)
    void eraseRange(int b, int e)
    void gamma(float)
    const FColor& get(int pos)
    int index(FColor)
    void insertRange(int b1, FColorList, int b2, int e2)
    FColorList interpolate(FColorList, float ratio, unsigned int smooth)
    void push_back(FColor)
    void resize(size_t size)
    void reserve(size_t size)
    void reverse()
    void scale(float)
    void set(int pos, FColor)
    void setAll(FColor)
    int size()
    void sort()
