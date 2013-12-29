#ifndef __ECHOMESH_COLOR_FCOLORLIST__
#define __ECHOMESH_COLOR_FCOLORLIST__

#include <algorithm>

#include "echomesh/color/FColor.h"

namespace echomesh {
namespace color {

class FColorList : public vector<FColor> {
 public:
  int count(const FColor& c) const {
    return std::count(begin(), end(), c);
  }

  void eraseOne(int pos) {
    erase(begin() + pos);
  }

  void eraseRange(int b, int e) {
    erase(begin() + b, begin() + e);
  }

  int index(const FColor& c) const {
    auto i = std::find(begin(), end(), c);
    return i == end() ? -1 : i - begin();
  }

  void insertRange(int b1, const FColorList& from, int b2, int e2) {
    insert(begin() + b1, from.begin() + b2, from.begin() + e2);
  }

  void reverse() {
    std::reverse(begin(), end());
  }

  void set(const FColor& color, int pos) {
    at(pos) = color;
  }

  void sort() {
    std::sort(begin(), end(), FColor::Comparer());
  }
};

}  // namespace color
}  // namespace echomesh

#endif  // __ECHOMESH_COLOR_FCOLORLIST__