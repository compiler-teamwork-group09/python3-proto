#!/usr/bin/env python3
# -- coding: utf8 --
# :author: nvagus
# :time: 1/12/18-10:25 PM
# :package: proto.test

from proto import Proto

with Proto() as person:
    def __proto_init__(self, name):
        self.name = name


    def introduce(self):
        print(f'my name is {self.name}')

alice = person('alice')
alice.introduce()


@alice.init
def personality(self, personality):
    self.personality = personality


with alice:
    def introduce(self):
        print(f'i am {self.personality} {self.name}')

small_alice = alice('small')
small_alice.introduce()
