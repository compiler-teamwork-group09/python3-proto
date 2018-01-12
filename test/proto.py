#!/usr/bin/env python3
# -- coding: utf8 --
# :author: nvagus
# :time: 12/22/17-3:47 PM
# :package: proto.test

import code

from proto import proto


@proto()
def person(self, name):
    self.name = name


@person.method()
def introduce(self):
    print(f'my name is {self.name}')


alice = person('alice')
alice.introduce()

code.interact(local=locals())
