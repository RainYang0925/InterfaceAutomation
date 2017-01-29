#coding:utf-8
import time


class DictObj(dict):
    """docstring for DictObj"""   
    def __setattr__(self, name, value):
        self[name] = value

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError, e:
            raise AttributeError(name)

def formatTime(t=1, seconds=None):
    tformat = {
        1: '%Y%m%d%H%M%S',
        2: '%Y-%m-%d %H:%M:%S',
        3: '%H:%M:%S'
    }
    if t == 3:
        if isinstance(seconds, int):
            ftime = time.strftime(tformat[t], time.gmtime(seconds))
        else:
            raise TypeError("arg seconds must be integer, default None")
    else:
        try:
            ftime = time.strftime(tformat[t], time.localtime())
        except KeyError, e:
            raise e
    return ftime



