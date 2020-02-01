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
import math


class Enemy:

    def __init__(self, ledstring, world, position=0, speed=0, wobble=0):
        self.ledstring = ledstring
        self.world = world
        self.position = position
        self.origin = position
        self.speed = speed
        self.wobble = wobble
        self.alive = False
        self.player_side = 0
        if "enemies" not in world:
            world["enemies"] = [self]
        else:
            world["enemies"].append(self)

    def draw(self):
        if self.alive:
            draw_pos = utils.range_constrain(self.position, 0, len(self.ledstring) - 1)
            self.ledstring[draw_pos].rgb((255, 0, 0))

    def tick(self, time):
        if not self.alive:
            return
        if self.wobble:
            self.position = self.origin + int(math.sin((time / 3000.0) * self.speed) * self.wobble)
        else:
            self.position += self.speed
            if self.position >= len(self.ledstring) or self.position < 0:
                self.alive = False

    def collide(self):
        if not self.alive:
            return
        if self.world["player"].attacking:
            player = self.world["player"]
            p_pos = player.position
            p_range = player.attack_width
            e_pos = self.position
            if e_pos > (p_pos - (p_range // 2)) and e_pos < (p_pos + (p_range // 2)):
                self.alive = False

    def spawn(self, position, speed, wobble=0):
        self.alive = True
        self.position = position
        self.origin = position
        self.speed = speed
        self.wobble = wobble
        if position > self.world["player"].position:
            self.player_side = 1
        else:
            self.player_side = -1
