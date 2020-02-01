#!/usr/bin/env -S python -u

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

import pygame
import sys
import LEDString
import Screensaver
import Player
import utils
import math


class Enemy:

    def __init__(self, ledstring, position, speed, wobble):
        self.ledstring = ledstring
        self.position = position
        self.origin = position
        self.speed = speed
        self.wobble = wobble
        self.alive = True

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

    def collide(self, world):
        if not self.alive:
            return
        if world["player"].attacking:
            player = world["player"]
            p_pos = player.position
            p_range = player.attack_width
            e_pos = self.position
            if e_pos > (p_pos - (p_range // 2)) and e_pos < (p_pos + (p_range // 2)):
                self.alive = False


def main():

    # TWANG globals
    led_size = 13
    led_margin = 1
    led_color = (0, 0, 0)
    led_string_length = 144
    led_string = LEDString.LEDString(led_string_length, color=led_color, size=led_size, margin=led_margin)
    led_string_status = 13
    screensaver = Screensaver.Screensaver(led_string)
    player = Player.Player(led_string)
    enemy = Enemy(led_string, 100, -10, 20)
    player_speed = 0
    world = {"player": player, "enemy": enemy}

    # pyGame stuff
    pygame.init()

    screen = pygame.display.set_mode((led_size * led_string_length, led_size + led_string_status))
    clock = pygame.time.Clock()
    pygame.display.set_caption('pyTWANG')
    font = pygame.font.Font(None, 20)

    # main loop
    running = True
    fps_limit = 60
    starttime = pygame.time.get_ticks()
    while running:
        clock.tick(fps_limit)
        time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_LEFT:
                    player_speed -= 1
                elif event.key == pygame.K_RIGHT:
                    player_speed += 1
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player.attack(time)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player_speed += 1
                elif event.key == pygame.K_RIGHT:
                    player_speed -= 1

        # Clear screen
        screen.fill((128, 128, 128))

        # Advance animations
        # led_string.animate()
        # screensaver.tick(time)
        led_string.clear()
        player.speed = player_speed
        player.tick(time)
        enemy.tick(time)
        enemy.collide(world)
        player.draw(time)
        enemy.draw()

        # Render LEDs onto the screen
        led_string.draw(screen)

        # Draw satusbar information
        status = font.render("t: {} s: {}".format((pygame.time.get_ticks() - starttime) // 1000, player_speed), True, (0, 0, 0))
        status_rect = status.get_rect()
        status_rect.topleft = (10, led_size)
        screen.blit(status, status_rect)

        # Make things visible
        pygame.display.flip()

    pygame.quit()
    sys.exit()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
