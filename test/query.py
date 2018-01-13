#!/usr/bin/env python3
# -- coding: utf8 --
# :author: nvagus
# :time: 1/13/18-9:54 AM
# :package: proto.test

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
