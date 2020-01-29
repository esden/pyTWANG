import pygame
import sys
import LEDString
import Screensaver


def range_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min;


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
        n = range_map(time - self.attack_millis, 0, self.attack_duration, 100, 5)
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


def main():

    # TWANG globals
    led_size = 13
    led_margin = 1
    led_color = (0, 0, 0)
    led_string_length = 144
    led_string = LEDString.LEDString(led_string_length, color=led_color, size=led_size, margin=led_margin)
    led_string_status = 13
    screensaver = Screensaver.Screensaver(led_string)
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
        player.draw(time)

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
