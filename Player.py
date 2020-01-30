# Copyright (c) 2020, Piotr Esden-Tempski <piotr@esden.net>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import utils

class Player:

    def __init__(self, ledstring, direction=1, attack_width=8, attack_duration=500):
        self.position = 0
        self.ledstring = ledstring
        self.direction = direction
        self.attack_width = attack_width
        self.attacking = False
        self.attack_millis = 0
        self.attack_duration = attack_duration
        self.speed = 0

    def draw(self, time):
        if not self.attacking:
            self.ledstring[self.position].rgb((0, 255, 0))
        else:
            self.__draw_attack(time)

    def __draw_attack(self, time):
        n = utils.range_map(time - self.attack_millis, 0, self.attack_duration, 100, 5)
        for i in range(self.position - (self.attack_width // 2) + 1, self.position + (self.attack_width //2) - 1):
            self.ledstring[i].rgb((0, 0, n))
        if n > 90:
            n = 255
            self.ledstring[self.position].rgb((255, 255, 255))
        else:
            n = 0
            self.ledstring[self.position].rgb((0, 255, 0))
        self.ledstring[self.position - (self.attack_width // 2)].rgb((n, n, 255))
        self.ledstring[self.position + (self.attack_width // 2)].rgb((n, n, 255))

    def tick(self, time):
        if self.attacking:
            if self.attack_millis + self.attack_duration < time:
                self.attacking = False
            return

        amount = self.speed * self.direction
        self.position += amount
        if self.position < 0:
            self.position = 0
        elif self.position >= len(self.ledstring):
            self.position = len(self.ledstring) - 1

    def attack(self, time):
        self.attack_millis = time
        self.attacking = True
