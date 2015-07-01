# coding: utf-8
__author__ = "João S. O. Bueno <gwidion@gmail.com>"
__version__ = "0.1"


from collections import defaultdict
from functools import partial

from threading import Thread



def _get_arg_names(func):
    return func.__code__.co_varnames[:func.__code__.co_argcount]

class Rule(object):
    def __init__(self, action, attrs=(),  predicate=None):
        self.action = action
        self.attrs = attrs if attrs else _get_arg_names(action)
        self.predicate = predicate
        if predicate:
            self.predicate_args = _get_arg_names(predicate)


class Reactor(object):
    _running = 0
    def __init__(self):
        self._rules = defaultdict(list)
        self._max_recursion = 1
        self._recursing = defaultdict(lambda: 0)
        self._tick = 0
        self._changed_at = {}
        self._running = True
        
    def _rule_setter(self, rule):
        for attrname in rule.attrs:
            self._rules[attrname].append(rule)

    def __setattr__(self, attrname, value):
        if callable(value):
            value = Rule(value)
        if isinstance(value, Rule):
            value.name = attrname
            self._rule_setter(value)
            self._exec_rule(value)
            return
        if not self._running or attrname in ("_tick", ):
            return super(Reactor, self).__setattr__(attrname, value)
        self._tick += 1
        self._changed_at[attrname] = self._tick
        if self._recursing[attrname] >= self._max_recursion:
            return
        self._recursing[attrname] += 1
        super(Reactor, self).__setattr__(attrname, value)
        for rule in self._rules[attrname]:
            self._exec_rule(rule)
        self._recursing[attrname] -= 1

    def encapsulate(self, func, attrs, run=True):
        kwargs = dict((name, getattr(self, name)) for name in attrs)
        if run:
            return func(**kwargs)
        return partial(func, **kwargs)
        
    def _exec_rule(self, rule):
        try:
            if (rule.predicate and
                not self.encapsulate(rule.predicate, rule.predicate_args)):
                return 
            result = self.encapsulate(rule.action, rule.attrs)
        except AttributeError:
            result = None
        setattr(self, rule.name, result)
            

            
R = Reactor()

class ThreadedReactor(Reactor):
    
    def _exec_rule(self, rule):
        try:
            if (rule.predicate and
                not self.encapsulate(rule.predicate, rule.predicate_args)):
                return 
            Thread(target=self._threaded_exec, args=[rule]).start()
        except AttributeError:
            setattr(self, rule.name, None)
    
    def _threaded_exec(self, rule):
        try:
            result = self.encapsulate(rule.action, rule.attrs)
        except AttributeError:
            result = None
        setattr(self, rule.name, result) 

TR = ThreadedReactor()

__doc__= """
>>> from react import R, Rule
>>> R.c = lambda a, b: a + b
>>> R.c
>>> R.a = 10
>>> R.b = 5
>>> R.c
15
>>> 
>>> R.d = Rule(lambda c: c * 2)
>>> R.d
30
>>> 
>>> R.a = -1
>>> 
>>> R.d
8
>>> R.e = lambda f: f / 2.
>>> R.f = lambda e: e * 2
Traceback (most recent call last):
    ...
TypeError: unsupported operand type(s) for *: 'NoneType' and 'int'
>>> R.e = 6
>>> R.f
12
>>> R.f = 20
>>> R.e
10.0
>>> R.g = Rule(lambda h: h.upper(), predicate= lambda h: isinstance(h, str))
>>> R.h = 5
>>> R.g is None
True
>>> R.h = "hello"
>>> R.g
'HELLO'
"""
