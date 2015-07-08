__author__ = 'gotlium'

import inspect
import mmc


class MonkeyProxy(object):
    def __init__(self, cls):
        monkey_bases = tuple(
            b._no_monkey for b in cls.__bases__ if hasattr(b, '_no_monkey'))
        for monkey_base in monkey_bases:
            for name, value in monkey_base.__dict__.iteritems():
                setattr(self, name, value)


def monkey_mix(cls, mixin):
    cls._no_monkey = MonkeyProxy(cls)
    is_bound_method = inspect.isfunction if mmc.PY3 else inspect.ismethod
    methods = inspect.getmembers(mixin, is_bound_method)

    for name, method in methods:
        if hasattr(cls, name):
            setattr(cls._no_monkey, name, getattr(cls, name))
        setattr(cls, name, method.im_func if mmc.PY2 else method)
