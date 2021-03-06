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


# A lot of this code is ported over from FastLED. This means that a lot of the color magic and the way things are
# handled is inherited from the Arduino/AVR C code. This is why we are working with 8bit integers most of the time.
# The descriptions are mostly also copied from the original FastLED code. So if you are confused about any of this
# I do recommend that you check the corresponding code in FastLED, it might shed some light on all of this. :)

class LED:

    def __init__(self, color=(0, 0, 0)):
        if isinstance(color, tuple):
            self.r, self.g, self.b = color
        elif isinstance(color, LED):
            self.r, self.g, self.b = color.r, color.b, color.b

    def rgb(self, color=None):
        if color:
            self.r, self.g, self.b = color

        return self.r, self.g, self.b

    def __add__(self, other):
        if isinstance(other, tuple):
            self.r = (self.r + other[0]) % 255
            self.g = (self.g + other[1]) % 255
            self.b = (self.b + other[2]) % 255
        elif isinstance(other, LED):
            self.r = (self.r + other.r) % 255
            self.g = (self.g + other.g) % 255
            self.b = (self.b + other.b) % 255
        else:
            raise TypeError("The RHS type is not supported.")

    def __str__(self):
        return f"({self.r}, {self.g}, {self.b})"

    def nhsv_spectrum(self, h, s, v):
        self.r, self.g, self.b = hsv_spectrum(h, s, v)
        return r, g, b

    def nhsv_rainbow(self, h, s, v):
        self.r, self.g, self.b = hsv_rainbow(h, s, v)
        return self.r, self.g, self.b

    def nscale8(self, scaler):
        self.r = scale8(self.r, scaler)
        self.g = scale8(self.g, scaler)
        self.b = scale8(self.b, scaler)


class LEDString:

    def __init__(self, length, color=(0, 0, 0), size=8, margin=1):
        self.leds = [LED(color) for _ in range(length)]
        self.color = color
        self.size = size
        self.margin = margin
        self.work_rect = pygame.Rect(margin, margin, size - margin * 2, size - margin * 2)

    def __setitem__(self, n, color):
        self.leds[n].rgb(color)

    def __getitem__(self, n):
        return self.leds[n]

    def __len__(self):
        return len(self.leds)

    def __str__(self):
        return "\n".join(self.leds)

    def draw(self, screen):
        self.work_rect.x = 1
        self.work_rect.y = 1
        color = pygame.Color(0, 0, 0)
        for led in self.leds:
            color.r = led.r
            color.g = led.g
            color.b = led.b
            pygame.draw.rect(screen, color.correct_gamma(0.5), self.work_rect)
            self.work_rect.move_ip(self.size, 0)

    def clear(self):
        for i in range(len(self.leds)):
            self.leds[i].rgb((0, 0, 0))

# scale one byte by a second one, which is treated as the numerator of a fraction whose denominator is 256
# In other words, it computes i * (scale / 256)


def scale8(val, scaler):
    ret = (val * scaler) // 255
    return ret


#  The "video" version of scale8 guarantees that the output will be only be zero if one or both of the inputs are zero.
#  If both inputs are non-zero, the output is guaranteed to be non-zero. This makes for better 'video'/LED dimming, at
#  the cost of several additional cycles.
def scale8_video(val, scaler):
    ret = ((val * scaler) >> 8)
    if val and scaler:
        ret += 1
    return ret


# HSV conversion constants
__hsv_section_6 = 0x40
__hsv_section_3 = 0x20


def __hsv_raw(h, s, v):
    # in spirit of c code we will wrap the values into the uint8 range
    h %= 256
    s %= 256
    v %= 256
    # print(f"h: {h} s: {s} v: {v}")

    # The brightness floor is minimum number that all of R, G, and Be will be set to.
    invs = 255 - s
    brightness_floor = (v * invs) // 256

    # The color amplitude is the maximum aumount of R, G, and B that will be added on top of the
    # brightness_floor to create the specific hue desired.
    color_amplitude = v - brightness_floor

    # Figuer out which section of the hue wheel we're in, and how far offset we are within that section
    section = h // LED.__hsv_section_3  # 0..2
    offset = h % LED.__hsv_section_3   # 0..63

    rampup = offset  # 0..63
    rampdown = (LED.__hsv_section_3 - 1) - offset  # 63..0

    # We now scale rampup and rampdown to a 0..255 range

    # This is redundant thus we fold it arithmetically into the later calculation.
    # # scale up to 255 range
    # # rampup *= 4; // 0..252
    # # rampdown *= 4 // 0..252

    # compute color-amplitude-scaled-down versions of rampup and rampdown
    rampup_amp_adj = (rampup * color_amplitude) // (256 // 4)
    rampdown_amp_adj = (rampdown * color_amplitude) // (256 // 4)

    # add brightness floor offset to everything
    rampup_adj_with_floor = rampup_amp_adj + brightness_floor
    rampdown_adj_with_floor = rampdown_amp_adj + brightness_floor

    # print(f"bf:{brightness_floor} ca:{color_amplitude} sec:{section} off:{offset} ru:{rampup} rd:{rampdown} "
    #       f"ruaa:{rampup_amp_adj} rdaa:{rampdown_amp_adj}¨ "
    #       f" ruawf: {rampup_adj_with_floor} rdawf: {rampdown_adj_with_floor}")

    if section:
        if section == 1:
            r = brightness_floor
            g = rampdown_adj_with_floor
            b = rampup_adj_with_floor
            # print(f"s1 {self.r} {self.g} {self.b}")
        else:
            r = rampup_adj_with_floor
            g = brightness_floor
            b = rampdown_adj_with_floor
            # print(f"s2 {self.r} {self.g} {self.b}")
    else:
        r = rampdown_adj_with_floor
        g = rampup_adj_with_floor
        b = brightness_floor
        # print(f"s0 {self.r} {self.g} {self.b}")

    return r, g, b


def hsv_spectrum(h, s, v):

    h = scale8(h, 191)
    return __hsv_raw(h, s, v)


def hsv_rainbow(h, s, v):

    # Yellow has a higher inherent brightness than any other color; pure yellow is perceived to be 93% as bright
    # as white. In order to make yellow appear the correct relative brightness, it has to be rendered brighter
    # than all other colors.
    # Level y1 is a moderate boost, the default.
    # Level y2 is a strong boost.
    y1 = True
    y2 = False

    # g2: Whether to divide all greens by two.
    # Depends greatly on your particular LEDs
    g2 = False

    # g_scale: what to scale green down by.
    # Depends GREATLY on your particular LEDs
    g_scale = 0

    # in spirit of c code we will wrap the values into the uint8 range
    h %= 256
    s %= 256
    v %= 256

    offset = h & 0x1F

    offset8 = (offset << 3) % 256

    third = scale8(offset8, (256 // 3))  # max = 85

    r, g, b = 0, 0, 0
    section = (h & 0xE0) >> 5
    if section == 0:
        # 000
        # case 0: R -> O
        r = 255 - third
        g = third
        b = 0
    elif section == 1:
        # 001
        # case 1: O -> Y
        if y1:
            r = 171
            g = 85 + third
            b = 0
        if y2:
            # twothirds = (third << 1);
            twothirds = scale8(offset8, ((256 * 2) // 3))  # max=170
            r = 170 + third
            g = 85 + twothirds
            b = 0
    elif section == 2:
        # 010
        # case 2: Y -> G
        if y1:
            # twothirds = (third << 1)
            twothirds = scale8(offset8, ((256 * 2) // 3))  # max = 170
            r = 171 - twothirds
            g = 170 + third
            b = 0
        if y2:
            r = 255 - offset8
            g = 255
            b = 0
    elif section == 3:
        # 011
        # case 3: G -> A
        r = 0
        g = 255 - third
        b = third
    elif section == 4:
        # 100
        # case 4: A -> B
        # twothirds = (third << 1);
        twothirds = scale8(offset8, ((256 * 2) // 3))  # max = 170
        r = 0
        g = 171 - twothirds  # 170?
        b = 85 + twothirds
    elif section == 5:
        # 101
        # case 5: B -> P
        r = third
        g = 0
        b = 255 - third
    elif section == 6:
        # 110
        # case 6: P - - K
        r = 85 + third
        g = 0
        b = 171 - third
    elif section == 7:
        # 111
        # case 7: # K -> R
        r = 170 + third
        g = 0
        b = 85 - third

    # print(f"sec: {section}")

    # This is one of the good places to scale the green down,
    # although the client can scale green down as well.
    if g2:
        g = g >> 1
    if g_scale:
        g = scale8_video(g, g_scale)

    # Scale down colors if we're desaturated at all
    # and add the brightness_floor to r, g, and b.
    if s != 255:
        if s == 0:
            r, g, b = 255, 255, 255
        else:
            # nscale8x3_video( r, g, b, sat)
            if r:
                r = scale8(r, s)
            if g:
                g = scale8(g, s)
            if b:
                b = scale8(b, s)

            desat = 255 - s
            desat = scale8(desat, desat)

            brightness_floor = desat
            r += brightness_floor
            g += brightness_floor
            b += brightness_floor

    # Now scale everything down if we're at value < 255.
    if v != 255:
        v = scale8_video(v, v)
        if v == 0:
            r, g, b = 0, 0, 0
        else:
            # nscale8x3_video( r, g, b, val)
            if r:
                r = scale8(r, v)
            if g:
                g = scale8(g, v)
            if b:
                b = scale8(b, v)

    return r, g, b
