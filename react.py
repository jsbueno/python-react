# coding: utf-8
from collections import defaultdict

class Rule(object):
    def __init__(self, action, attrs=(),  predicate=None):
        self.action = action
        self.attrs = attrs if attrs else action.__code__.co_varnames[:action.__code__.co_argcount]
        self.predicate = predicate


class Reactor(object):
    _running = 0
    def __init__(self):
        self._rules = defaultdict(list)
        self._max_recursion = 1
        self._recursing = defaultdict(lambda: 0)
        self._running = True
        
    def _rule_setter(self, rule):
        for attrname in rule.attrs:
            self._rules[attrname].append(rule)

    def __setattr__(self, attrname, value):
        if isinstance(value, Rule):
            value.name = attrname
            self._rule_setter(value)
            self._exec_rule(value)
            return
        if not self._running:
            return super(Reactor, self).__setattr__(attrname, value)
        if self._recursing[value] >= self._max_recursion:
            return
        self._recursing[value] += 1
        super(Reactor, self).__setattr__(attrname, value)
        for rule in self._rules[attrname]:
            self._exec_rule(rule)
        self._recursing[value] -= 1

    def _exec_rule(self, rule):
        try:
            result =  rule.action(**dict((name, getattr(self, name)) for name in rule.attrs))
        except AttributeError:
            result = None
        setattr(self, rule.name, result)
            
            
R = Reactor()

__doc__= """
>>> from react import R, Rule
>>> R.c = Rule(lambda a, b: a + b)
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
>>> R.e = Rule(lambda f: f / 2.)
>>> R.f = Rule(lambda e: e * 2)
Traceback (most recent call last):
    ...
TypeError: unsupported operand type(s) for *: 'NoneType' and 'int'
>>> R.e = 6
>>> R.f
12
>>> R.f = 20
>>> R.e
10.0
"""
