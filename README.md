# Python3-proto: a type system
## 1. Requirement
+ python >= 3.6.0

## 2. Features
+ Multiple inheritance.
+ Recusion instantiation.
+ Convenient and fast implemented.
+ Descriptor supported.
+ Each instance is evenly regarded as a class, as well as a meta class.
+ Each instance is both an instance of Proto, as well as a subclass of Proto.

## 3. Examples
### 3.1. Using wrappers to create
```python
from proto import proto

@proto()
def person(self, name):
    self.name = name


@person.method
def introduce(self):
    print(f'my name is {self.name}')


alice = person('alice')
alice.introduce()
```
### 3.3. Combine several instances into a single one
``` python
from proto import proto, combine

@proto()
def person(self, name):
    self.name = name


alice = person('alice')
bob = person('bob')


@alice.class_method
def introduce(self):
    print(f'my name is {self.__name__}')


@bob.static_method
def greeting():
    print('nice to meet you')


superman = combine(alice, bob, name='superman')
superman.introduce()
superman.greeting()
```
 
### 3.3. Using default 'with' statement to quickly build a target
``` python
from proto import Proto

with Proto() as person:
    def __proto_init__(self, name):
        self.name = name


    def introduce(self):
        print(f'my name is {self.name}')

alice = person('alice')
alice.introduce()
```

### 3.4. Implement hooks
``` python
from proto import proto

@proto()
def person(self, name):
    self.name = name


@person.enter
def enter_person(self):
    print(f'hello everyone, my name is {self.name}')
    return self


@person.exit
def exit_person(*_):
    print('bye bye')


@person.getitem
def getitem_person(self, item):
    return getattr(self, item)


@person.setitem
def setitem_person(self, key, value):
    return setattr(self, key, value)


with person('alice') as alice:
    alice['lover'] = person('bob')
    print(f"my lover is {alice['lover'].name}")
```

## 4. Advanced usage
## 4.1. Attribute searching path
Python's \__mro__ hook is not implemented since each instance has both its bases and its meta. We actually search an attribute from the meta prior to the bases. If the bases were added to the \__mro__ or \__bases__, there would be a dilemma that either we would pass the bases to the meta or the \__mro__ is not used, because we would only search the mata  according to \__mro__ when we have already raise an attribute error. Ultimately, it is for the fact that \__mro__ is an attribute for a type but not an object.

We have implemented four different type of searching, yet only single process are there with switches. There are four user interfaces: normally getattr, super, method_only, super_method_only. An example of using super is as follows:
``` python
from proto import proto

@proto()
def family(self, sir):
    self.sir = sir


@proto(family)
def person(self, sir, name):
    self.super(self).__proto_init__(sir)
    self.name = name
```

## 4.2. Query for type information

Python's isinstance and issubclass is not perfectly worked here since we have modified the logic of the type system. Therefore, we have other tools to help users to explore the relationship between two classes. There are two user interfaces: is_instance and is_subclass. We continue the prior example:
``` python
from proto import Proto
from proto import proto
from proto import is_instance, is_subclass


@proto()
def family(self, sir):
    self.sir = sir


@proto(family)
def person(self, sir, name):
    self.super(self).__proto_init__(sir)
    self.name = name


@family.method
def introduce(self):
    print(f'my sir name is {self.sir}')


@person.method
def introduce(self):
    self.super(self).introduce()
    print(f'my own name is {self.name}')


alice = person('alice', 'bob')
alice.introduce()

print(is_instance(alice, family))
print(is_subclass(person, family))
print(is_instance(family, alice))
print(is_subclass(alice, Proto))
```

## 4.3. Native interfaces
To create a new Proto type, since Proto is a meta type, the native way is to instance is directly.
``` python
# this is not the real signature, but can be regarded as this one
Proto(mcs, *args, __name__='Anonymous Proto', __super__=(Proto), **kwargs):
	return type(mcs, __name__, __super__, {})
```
Where, args and kwargs should be passed to \__init__ and the passed to \__proto_init__. If you would like to build an instance from this native call, remember that \__name__ and \__super__ will not passed to your init function.

## 4.4. Classmethod and Staticmethod
There are three classes, Method, Classmethod, Staticmethod, where the last two are subclasses of Method, could be used as decorator to create method. Those can be used when you use default 'with' statement to add attrbutes.
Meanwhile, each instance has properties like