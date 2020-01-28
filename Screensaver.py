import random
import math


class Screensaver:

    # these are dots in bowl parameters
    dotspeed = 22
    dots_in_bowls_count = 3
    dot_distance = 65535 / dots_in_bowls_count
    dot_brightness = 255

    def __init__(self, ledstring):
        self.ledstring = ledstring

    def tick(self, time):
        mode = int(time / 30000) % 5
        # mode = 4
        ledstring = self.ledstring

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

            for i in range(Screensaver.dots_in_bowls_count):
                mm = (((i * Screensaver.dot_distance) + (time % (2 ** 32)) * Screensaver.dotspeed) % (2 ** 16)) / (2 ** 15)
                n = int((((math.sin(mm * math.pi) + 1) / 2) * (len(ledstring) - 5)) + 2)
                c = int(mm * 128)
                # print(f"mm {mm} n {n} c {c}")
                ledstring[n - 2].hsv_rainbow((c, 255, Screensaver.dot_brightness // 4))
                ledstring[n - 1].hsv_rainbow((c, 255, Screensaver.dot_brightness // 2))
                ledstring[n + 0].hsv_rainbow((c, 255, Screensaver.dot_brightness))
                ledstring[n + 1].hsv_rainbow((c, 255, Screensaver.dot_brightness // 2))
                ledstring[n + 2].hsv_rainbow((c, 255, Screensaver.dot_brightness // 4))

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