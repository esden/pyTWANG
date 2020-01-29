import pygame
import sys
import LEDString
import Screensaver
import Player


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
