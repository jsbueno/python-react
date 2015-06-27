Python React
=============


A Reactive Programming core for Python
---------------------------------------


Started as a sample on how Python's attibute models
allow for intelligent objects in a presentation,
the aim of this module is to become a simple, yet
powerful helper for reactive programming in Python.

Check https://en.wikipedia.org/wiki/Reactive_programming
for more on reactive programing.

The simple principle is to leverage on Python's '''__setattr__'''
hook to both stablish propagating rules and apply rules on attribute
change.

Usage
-----

Simply instantiate a react.Reactor class - any assignment
of a function or react.Rule class to an attribute on this
class will create a new Rule - each time an attribute
with the same name as the parameters on this function
(or ```attrs``` parameter for a Rule) is assigned
a new (non-Rule) value, the Rule action is called
with that value (and the values for other parameters
it depends on).

For a fast start on quick hacks, there is an
"R" reactor instance ready to use:

For example:
'''

>>> from react import R
>>> 
>>> R.greeting = lambda name, age: "Hello {}! How  nice you are {} years old!".format(name, age)
>>> R.name = "João"
>>> R.age = 40
>>> R.greeting
'Hello João! How  nice you are 40 years old!'
>>> R.age = 25
>>> R.greeting
'Hello João! How  nice you are 25 years old!'
'''

A couple things to take note for now:
1.  Although the simple rule examples are with
    lambda functions, the Rule callable can be an arbitrary
    Python callable - even making I/O or network calls
    with any values.

2.  Any created rules are independent of the actual value
    stored in the attributes. They are stored, and can be read
    as they are set by their name, using ```getattr``` or
    the instance's ```__dict__```.  The rules are kept in a
    `_rules` data structure on the instance.  This is much like
    a spreadsheet where one does see the calculated values, but not
    the underlying formulas for each cell.
   
 3.  The propagation on the current Reactor class is synchronous: when
    an attribute is set on the instance, all rules are checked
    and calculated before the execution flow comes back to the
    frame where the assignment statement took place.
   
Compatibility:
---------------
The code so far has been tested with cPython 2.7, cPython 3.4
and pypy 2.4.0 - shour work fine for other Python implementations.

There are simple doctests (which also serve as examples)  in the main file -
run them with
```python -m doctest react.py```


TODO:
------
This is still an incipient project - if you see have
any possible usage for this, please jump in for
colaboration.

Next steps are: better and more complete examples,
possibility to watch over structured values
like lists and dicts (probably using
proxies for those), asynchronous value propagation,
and the possibility to do interprocess value propagation
(with a to-be-decided trasnport channel like memcached, celery, etc...)

COPYING:
--------
All code in this project is licensed under the GNU Lesse General Public License 3.0 or later:
attribution required and share alike.

