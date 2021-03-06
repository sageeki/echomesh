# include "echomesh/util/AppCallback.pyx"

from libcpp cimport bool
from libcpp.string cimport string

cdef extern from "echomesh/util/EchomeshApplication.h" namespace "echomesh":
    void startApplication(StringCaller cb, void* user_data) nogil
    bool isStarted()

cdef extern from "echomesh/util/Quit.h" namespace "echomesh":
    void quit() nogil

def start_application(f):
    if f:
        callback = <void*> f
    else:
        callback = NULL
    with nogil:
        startApplication(perform_string_callback, callback)

def stop_application():
    quit()

def is_started():
    return isStarted()
