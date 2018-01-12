#!/usr/bin/env python3
# -- coding: utf8 --
# :author: nvagus
# :time: 1/12/18-10:38 PM
# :package: proto.test

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
