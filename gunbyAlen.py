from random import choice
from random import randint
import pygame
from math import *

FPS = 30
v_g = 5  # skorost pushki
number_of_targets = 4  # kolvo targetov
number_of_stargets = 2  # kolvo special targetov
counter = 0

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
BLOOD = (200, 0, 0)
GAME_COLORS = [RED, BLUE, GREEN, MAGENTA, (155, 230, 132), (0, 234, 140)]

WIDTH = 800  # widtth ekran
HEIGHT = 600  # height ekran


def rotate_rect(scr, x, y, a, b, alf, color):
    pygame.draw.polygon(scr, color, [(x, y), (x + a * cos(alf), y + a * sin(alf)),
                                     (x + a * cos(alf) - b * sin(alf), y + a * sin(alf) + b * cos(alf)),
                                     (x - b * sin(alf), y + b * cos(alf)), (x, y)])


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = gun.gunpos
        self.y = HEIGHT - 50
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30
        self.acceleration = 0.98
        self.bullettype = 1

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        self.vy -= self.acceleration
        self.x += self.vx
        self.y -= self.vy
        if self.x <= 0:
            self.vx = self.vx * (-1)
        if self.x >= WIDTH:
            self.vx = self.vx * (-1)
        if self.y <= 0:
            self.vy = self.vy * (-1)
        if self.y >= HEIGHT:
            self.vy = self.vy * (-1)

    def move_2(self):
        self.vy += self.acceleration
        self.x += self.vx
        self.y -= self.vy
        if self.x <= 0:
            self.vx = self.vx * (-1)
        if self.x >= WIDTH:
            self.vx = self.vx * (-1)
        if self.y <= 0:
            self.vy = self.vy * (-1)
        if self.y >= HEIGHT:
            self.vy = self.vy * (-1)

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj, i):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение. i -i sharik
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        # FIXME
        if (self.x - obj.x[i]) ** 2 + (self.y - obj.y[i]) ** 2 <= (self.r + obj.r[i]) ** 2:
            return True
        else:
            return False

    def bombhittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + 15) ** 2:
            return True

        else:
            return False


class Gun:
    def __init__(self, screen, lives):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.gunpos = WIDTH / 2
        self.lives = lives

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * cos(self.an)
        new_ball.vy = - self.f2_power * sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if event.pos[1] < HEIGHT - 50:
                self.an = -acos((event.pos[0] - self.gunpos) / sqrt(
                    (event.pos[1] - HEIGHT + 50) ** 2 + (event.pos[0] - self.gunpos) ** 2))
            else:
                self.an = acos((event.pos[0] - self.gunpos) / sqrt(
                    (event.pos[1] - HEIGHT + 50) ** 2 + (event.pos[0] - self.gunpos) ** 2))

        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):

        rotate_rect(self.screen, self.gunpos, HEIGHT - 50, 15, 100, -pi / 2 + self.an, GREY)
        rotate_rect(self.screen, self.gunpos, HEIGHT - 50, 15, self.f2_power, -pi / 2 + self.an, self.color)
        pygame.draw.rect(self.screen, GREY, (self.gunpos - 50, HEIGHT - 65, 100, 50))

    def draw2(self):

        rotate_rect(self.screen, self.gunpos, HEIGHT - 50, 15, 100, -pi / 2 + self.an, GREY)
        rotate_rect(self.screen, self.gunpos, HEIGHT - 50, 15, self.f2_power, -pi / 2 + self.an, self.color)
        pygame.draw.rect(self.screen, GREY, (self.gunpos - 50, HEIGHT - 65, 100, 50))

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY

    def gun_movement(self):

        global v_g
        self.gunpos += v_g
        if self.gunpos <= 50:
            v_g = v_g * (-1)
        if self.gunpos >= WIDTH - 50:
            v_g = v_g * (-1)

    def draw_lives(self):
        for i in range(self.lives):
            pygame.draw.circle(self.screen, BLOOD, (WIDTH / 2 + 20 * (2 * i - self.lives / 2), 575), 15)
            f1 = pygame.font.Font(None, 50)
            text1 = f1.render('Hp', True, (180, 0, 0))
            screen.blit(text1, (WIDTH / 2 + 30 * (2 * i - self.lives / 2), 575 - 40))

    def gun_hit(self):
        self.lives -= 1
        if self.lives > 0:
            return False
        else:
            return True


class Target:
    def __init__(self):
        self.screen = screen
        self.x = []
        self.y = []
        self.color = (0, 0, 0)
        self.r = []
        self.velx = []
        self.vely = []

    def kill(self):
        self.points = 0
        self.live += 1
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        self.x.append(randint(100, WIDTH - 100))
        self.y.append(randint(100, HEIGHT - 175))
        self.r.append(randint(5, 25))
        self.velx.append(randint(-5, 5))
        self.vely.append(randint(-5, 5))
        self.color = YELLOW

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points = points
        self.x = self.x[:i] + self.x[i + 1:]
        self.y = self.y[:i] + self.y[i + 1:]
        self.r = self.r[:i] + self.r[i + 1:]
        return 1

    def draw(self, i):
        self.x[i] += self.velx[i]
        self.y[i] += self.vely[i]
        if self.x[i] < self.r[i] or self.x[i] > WIDTH - self.r[i]:
            self.velx[i] = self.velx[i] * (-1)
        if self.y[i] < self.r[i] or self.y[i] > HEIGHT - 150 - self.r[i]:
            self.vely[i] = self.vely[i] * (-1)
        pygame.draw.circle(self.screen, self.color, (self.x[i], self.y[i]), self.r[i])


class SpecialTarget(Target):
    def __init__(self):
        super().__init__()

    def kill(self):
        self.slive += 1
        self.new_target()

    def new_target(self):
        self.x.append(randint(100, WIDTH - 100))
        self.y.append(randint(100, HEIGHT - 175))
        self.r.append(randint(5, 25))
        self.velx.append(randint(-5, 5))
        self.vely.append(randint(-5, 5))
        self.color = CYAN

    def draw(self, i):
        self.x[i] += self.velx[i]

        if self.x[i] < self.r[i] or self.x[i] > WIDTH - self.r[i]:
            self.velx[i] = self.velx[i] * (-1)
        if self.y[i] < self.r[i] or self.y[i] > HEIGHT - 150 - self.r[i]:
            self.vely[i] = self.vely[i] * (-1)
        pygame.draw.circle(self.screen, self.color, (self.x[i], self.y[i]), self.r[i])

    def hit(self):

        self.x = self.x[:i] + self.x[i + 1:]
        self.y = self.y[:i] + self.y[i + 1:]
        self.r = self.r[:i] + self.r[i + 1:]
        return 2


class Bomb(Ball, Target):
    def __init__(self):
        super().__init__(screen)
        self.acceleration = 0.98 / 3
        self.screen = screen
        self.x = randint(0, WIDTH)
        self.y = 20
        self.vx = 0
        self.vy = 0
        self.color = BLACK

    def create(self):
        global bombs
        new_bomb = Bomb()
        bombs.append(new_bomb)

    def move(self):
        global bombs
        self.vy += self.acceleration
        self.y += self.vy
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), 10)
        if self.y > HEIGHT:
            bombs = bombs[1:]

    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.r)


pygame.init()
bg=pygame.image.load("table.png")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []
bombs = []
clock = pygame.time.Clock()
gun = Gun(screen, lives=5)


target = Target()
spec_target = SpecialTarget()
bomb = Bomb()
target.live = 0
spec_target.slive = 0
bullet_type = 1
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    gun.draw_lives()

    while target.live < number_of_targets:
        target.kill()
    while spec_target.slive < number_of_stargets:
        spec_target.kill()
    for i in range(target.live):
        target.draw(i)
    for i in range(spec_target.slive):
        spec_target.draw(i)

    if randint(1, 25) == 12:  # chtobi bombi ne kazsdii sec fps povt
        bomb.create()
    for b in balls:  # otrisovka snaryadov
        b.draw()
    for bomb in bombs:
        bomb.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:

            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)

        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)


        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                bullet_type = 1
            elif event.key == pygame.K_2:
                bullet_type = 2
    # snaryadi s norm graviti dlya isp nazhmi 1
    if bullet_type == 1:
        for b in balls:
            b.move()
            for i in range(number_of_targets):
                if b.hittest(target, i) and target.live and bullet_type == 1:
                    target.live -= 1
                    counter += target.hit()
                    target.kill()
                    b.vx = 0
                    b.x = -20
            for i in range(number_of_stargets):
                if b.hittest(spec_target, i) and target.live > 0 and bullet_type == 2:
                    spec_target.slive -= 1
                    counter += spec_target.hit()
                    shots_counter = 0
                    spec_target.kill()
    # snaryadi s ne norm graviti dlya isp nazhmi 2
    if bullet_type == 2:
        for b in balls:
            b.move_2()
            for i in range(number_of_targets):
                if b.hittest(target, i) and target.live and bullet_type == 2:
                    target.live -= 1
                    counter += target.hit()
                    target.kill()
                    b.vx = 0
                    b.x = -20
            for i in range(number_of_stargets):
                if b.hittest(spec_target, i) and target.live > 0 and bullet_type == 2:
                    spec_target.slive -= 1
                    counter += spec_target.hit()
                    shots_counter = 0
                    spec_target.kill()
                    b.vx = 0
                    b.x = 20
    for bomb in bombs:
        for b in balls:
            if b.bombhittest(bomb):
                bombs = bombs[:bombs.index(bomb)] + bombs[bombs.index(bomb) + 1:]
                balls = balls[:balls.index(b)] + balls[balls.index(b) + 1:]
        bomb.move()
        if bomb.x <= gun.gunpos + 50 and bomb.x >= gun.gunpos - 50:
            if bomb.y <= HEIGHT - 65 and bomb.y >= HEIGHT - 65 - 25:
                bombs = bombs[:bombs.index(bomb)] + bombs[bombs.index(bomb) + 1:]
                if gun.gun_hit():
                    finished = True
    gun.gun_movement()
    gun.power_up()

while finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = False
    f1 = pygame.font.Font(None, 50)
    text2 = f1.render('Score=' + str(counter), True, (180, 0, 0))
    screen.blit(text2, (WIDTH / 2, HEIGHT / 2))
    pygame.display.update()
pygame.quit()
print("na 1-odin tip patronov, na 2 vtoroyoy tip, zheltii shariki mozhno popast tolko 2 tipom")