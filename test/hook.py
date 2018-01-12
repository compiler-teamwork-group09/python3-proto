#!/usr/bin/env python3
# -- coding: utf8 --
# :author: nvagus
# :time: 1/12/18-11:03 PM
# :package: proto.test

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
