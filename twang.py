import pygame
import sys
import math


class LEDString:

    def __init__(self, length, color=(0, 0, 0), size=8, margin=1):
        self.leds = [list(color) for n in range(length)]
        self.color = color
        self.size = size
        self.margin = margin
        self.work_rect = pygame.Rect(margin, margin, size - margin * 2, size - margin * 2)

    def __setitem__(self, n, color):
        self.leds[n] = color

    def __getitem__(self, n):
        return self.leds[n]

    def __len__(self):
        return len(self.leds)

    def __str__(self):
        return "\n".join(f"({led[0]}, {led[1]}, {led[2]})" for led in self.leds)

    def draw(self, screen):
        self.work_rect.x = 1
        self.work_rect.y = 1
        for led in self.leds:
            pygame.draw.rect(screen, led, self.work_rect)
            self.work_rect.move_ip(self.size,0)

    def animate(self):
        self.leds[0][0] += 1
        self.leds[0][0] %= 255


def nscale8(color, scaler):
    """
    Scale a color by multiplying all colors by (scaler/256)
    :param color:
    :param scaler:
    :return: color
    """
    return tuple(int(val * (scaler / 256)) for val in color)


def hsv_to_rgb(h, s, v):
    color = pygame.Color(255, 0, 0)
    color.hsva = ((h / 256) * 360, (s / 256) * 100, (v / 256) * 100, 100)
    return color.r, color.g, color.b


def screensaver_tick(ledstring, time):
    mode = int(time / 30000) % 5

    # print(f"m: {mode}")
    if mode == 0:
        for i in range(len(ledstring)):
            ledstring[i] = nscale8(ledstring[i], 250)

        n = int((time / 250) % 10)
        c = int(20 + ((math.sin(math.radians(time / 5000.00)) * 255 + 1) * 33)) % 256
        # print(f"t: {time / 5000.00} c: {c}")
        for i in range(len(ledstring)):
            if i % 10 == n:
                ledstring[i] = hsv_to_rgb(c, 255, 150)
            i += 1
    elif mode == 1:
        ledstring[0] = (0, 255, 0)
    elif mode == 2:
        ledstring[0] = (0, 0, 255)
    elif mode == 3:
        ledstring[0] = (255, 0, 255)
    elif mode == 4:
        ledstring[0] = (255, 255, 0)
    else:
        ledstring[0] = (255, 0, 0)
        ledstring[1] = (255, 0, 0)


def main():

    # TWANG globals
    led_size = 16
    led_margin = 1
    led_color = (0, 0, 0)
    led_string_length = 144
    led_string = LEDString(led_string_length, color=led_color, size=led_size, margin=led_margin)

    # pyGame stuff
    pygame.init()

    screen = pygame.display.set_mode((led_size * led_string_length, led_size))
    clock = pygame.time.Clock()
    pygame.display.set_caption('pyTWANG')

    # main loop
    running = True
    fps_limit = 60
    starttime = pygame.time.get_ticks()
    while running:
        clock.tick(fps_limit)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        # led_string.animate()
        screensaver_tick(led_string, pygame.time.get_ticks())
        led_string.draw(screen)

        pygame.display.flip()
        #print("t: {}".format((pygame.time.get_ticks() - starttime) / 1000))

    pygame.quit()
    sys.exit()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__ == "__main__":
    # call the main function
    main()
