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


def monkey_mix(cls, mixin, methods=None):
    assert '_no_monkey' not in cls.__dict__, 'Multi monkey mix not supported'
    cls._no_monkey = MonkeyProxy(cls)

    if methods is None:
        isboundmethod = inspect.isfunction if mmc.PY3 else inspect.ismethod
        methods = inspect.getmembers(mixin, isboundmethod)
    else:
        methods = [(m, getattr(mixin, m)) for m in methods]

    for name, method in methods:
        if hasattr(cls, name):
            setattr(cls._no_monkey, name, getattr(cls, name))
        setattr(cls, name, method.im_func if mmc.PY2 else method)
