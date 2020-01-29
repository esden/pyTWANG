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
