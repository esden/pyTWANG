import pygame
import sys
import math
import random
import LEDString


class Player:

    def __init__(self, ledstring, direction=1):
        self.position = 0
        self.ledstring = ledstring
        self.direction = direction

    def draw(self):
        self.ledstring[self.position].rgb((0, 255, 0))

    def move(self, speed):
        amount = speed * self.direction
        self.position += amount
        if self.position < 0:
            self.position = 0
        elif self.position >= len(self.ledstring):
            self.position = len(self.ledstring) - 1


# these are screensaver Mode 2 consts
# TODO: refactor, to put the screensaver in a class
screensaver_dotspeed = 22
screensaver_dots_in_bowls_count = 3
screensaver_dot_distance = 65535 / screensaver_dots_in_bowls_count
screensaver_dot_brightness = 255


def screensaver_tick(ledstring, time):
    mode = int(time / 30000) % 5
    # mode = 4

    # print(f"m: {mode}")
    if mode == 0:
        # Marching green <> orange
        for led in ledstring:
            led.nscale8(250)

        n = int((time / 250) % 10)
        c = int(20 + ((math.sin(math.radians(time / 5000.00)) * 255 + 1) * 33)) % 256
        # print(f"t: {time / 5000.00} c: {c}")
        for i in range(len(ledstring)):
            if i % 10 == n:
                result = ledstring[i].hsv_rainbow((c, 255, 150))
        # print(result)

    elif mode == 1:
        # Random flashes
        for led in ledstring:
            led.nscale8(250)

        for i in range(len(ledstring)):
            if random.randrange(0, 20) == 0:
                ledstring[i].hsv_rainbow((25, 255, 100))

    elif mode == 2:
        # dots in bowl
        ledstring.clear()

        for i in range(screensaver_dots_in_bowls_count):
            mm = (((i * screensaver_dot_distance) + (time % (2 ** 32)) * screensaver_dotspeed) % (2 ** 16)) / (2 ** 15)
            n = int((((math.sin(mm * math.pi) + 1) / 2) * (len(ledstring) - 5)) + 2)
            c = int(mm * 128)
            # print(f"mm {mm} n {n} c {c}")
            ledstring[n - 2].hsv_rainbow((c, 255, screensaver_dot_brightness // 4))
            ledstring[n - 1].hsv_rainbow((c, 255, screensaver_dot_brightness // 2))
            ledstring[n + 0].hsv_rainbow((c, 255, screensaver_dot_brightness))
            ledstring[n + 1].hsv_rainbow((c, 255, screensaver_dot_brightness // 2))
            ledstring[n + 2].hsv_rainbow((c, 255, screensaver_dot_brightness // 4))

    elif mode == 3:
        # Sparkles
        for led in ledstring:
            led.nscale8(128)

        c = time % 800
        if c < 240:
            n = 121 - c // 2
        else:
            n = 1

        for i in range(len(ledstring)):
            if random.randrange(0, 256) <= n:
                ledstring[i].rgb((100, 100, 100))

    else:
        # Scroll dots
        for i in range(len(ledstring)):
            if (i + (time // 100)) % 5 == 0:
                ledstring[i].rgb((100, 100, 100))
            else:
                ledstring[i].rgb((0, 0, 0))


def main():

    # TWANG globals
    led_size = 13
    led_margin = 1
    led_color = (0, 0, 0)
    led_string_length = 144
    led_string = LEDString.LEDString(led_string_length, color=led_color, size=led_size, margin=led_margin)
    led_string_status = 13
    player = Player(led_string)
    player_speed = 0

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

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_LEFT:
                    player_speed = -1
                elif event.key == pygame.K_RIGHT:
                    player_speed = 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_speed = 0

        # Clear screen
        screen.fill((128, 128, 128))

        # Advance animations
        # led_string.animate()
        # screensaver_tick(led_string, pygame.time.get_ticks())
        led_string.clear()
        player.draw()
        player.move(player_speed)

        # Render LEDs onto the screen
        led_string.draw(screen)

        # Draw satusbar information
        status = font.render("t: {}".format((pygame.time.get_ticks() - starttime) / 1000), True, (0, 0, 0))
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
