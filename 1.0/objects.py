from settings import *
from math import floor
from random import randint
import pygame as pg


def rect_rect_intersect(r1, r2):
    return r1.x <= r2.x + r2.w and r1.x + r1.w >= r2.x and\
           r1.y <= r2.y + r2.h and r1.y + r1.h >= r2.y

class Almaz:
    def __init__(self, x, y):
        self.x, self.y = x * CELL_WIDTH, y * CELL_HEIGHT # позиция
        self.anim_pos = randint(0, len(ANIMATIONS[0]) - 1) # смещение в анимации(кадр)

    def draw(self, surf):
        surf.blit(TEXTURES[ANIMATIONS[0][floor(self.anim_pos)]][1], (self.x, self.y))
        self.anim_pos += 0.05
        self.anim_pos %= len(ANIMATIONS[0])


class Player:
    def __init__(self, x, y):
        self.x, self.y = x * CELL_WIDTH, y * CELL_HEIGHT
        self.anim_pos = 0
        self.anim = 1 # индекс анимации в массиве ANIMATIONS
        self.fire_timer = 0

    def draw(self, surf):
        surf.blit(TEXTURES[ANIMATIONS[self.anim][floor(self.anim_pos)]][1], (self.x, self.y))
        self.anim_pos += 0.05
        self.anim_pos %= len(ANIMATIONS[self.anim])

    def move(self, dx, dy):
        my_rect = pg.Rect((self.x + 15 + dx, self.y + 2 + dy, CELL_WIDTH - 30, CELL_HEIGHT - 3))

        for i in map_now:
            if i[0] == TEXTURES[1][1]:
                other_rect = pg.Rect((i[1][0], i[1][1], CELL_WIDTH, CELL_HEIGHT))

                # noinspection PyTypeChecker
                if rect_rect_intersect(my_rect, other_rect):
                    if not dx == 0:
                        dx = 0

                    if not dy == 0:
                        dy = 0

        self.x += dx * PLAYER_SPEED
        self.y += dy * PLAYER_SPEED

    def is_on_floor(self):
        my_rect = pg.Rect((self.x + 2, self.y + 2 + 2, CELL_WIDTH - 2, CELL_HEIGHT - 3))

        for i in map_now:
            if i[0] == TEXTURES[1][1]:
                other_rect = pg.Rect((i[1][0], i[1][1], CELL_WIDTH, CELL_HEIGHT))

                # noinspection PyTypeChecker
                if rect_rect_intersect(my_rect, other_rect):
                    return True

        return False

    def is_on_stairs(self, dx):
        d = dx * (CELL_WIDTH / 3) if dx else 0
        my_rect1 = pg.Rect((self.x + CELL_WIDTH/2 - d, self.y + CELL_HEIGHT / 2, 1, 1))
        my_rect2 = pg.Rect((self.x + CELL_WIDTH/2 - d, self.y + CELL_HEIGHT, 1, 1))

        for i in map_now:
            if i[0] == TEXTURES[2][1]:
                other_rect = pg.Rect((i[1][0], i[1][1], CELL_WIDTH, CELL_HEIGHT))

                # noinspection PyTypeChecker
                if rect_rect_intersect(my_rect1, other_rect) or rect_rect_intersect(my_rect2, other_rect):
                    return True

        return False

    # для алмазов, монстров и двери
    def check_collision(self, objects):
        my_rect = pg.Rect((self.x + 5, self.y + 2, CELL_WIDTH - 7, CELL_HEIGHT - 3))

        for i in objects:
            other_rect = pg.Rect((i.x, i.y, CELL_WIDTH, CELL_HEIGHT))

            # noinspection PyTypeChecker
            if rect_rect_intersect(my_rect, other_rect):
                if isinstance(i, (Almaz, Door, Monstr)):
                    return i

    def control(self, keys):
        last_anim = self.anim
        if not self.is_on_floor() and not self.is_on_stairs(0):
            self.anim = 7
            self.move(0, 1)
        elif "fire_left" in keys:
            if self.fire_timer == 0:
                self.anim = 5
                bullets.append(Bullet(self.x, self.y + CELL_HEIGHT // 2, -1))
                self.fire_timer = 120
        elif "fire_right" in keys:
            if self.fire_timer == 0:
                self.anim = 6
                bullets.append(Bullet(self.x + CELL_WIDTH, self.y + CELL_HEIGHT // 2, 1))
                self.fire_timer = 120
        elif "left" in keys:
            self.anim = 2
            self.move(-1, 0)
        elif "right" in keys:
            self.anim = 3
            self.move(1, 0)
        elif "up" in keys and self.is_on_stairs(-1):
            self.anim = 4
            self.move(0, -1)
        elif "down" in keys and self.is_on_stairs(1):
            self.anim = 4
            self.move(0, 1)
        else:
            self.anim = 1

        if not self.anim == last_anim:
            self.anim_pos = 0

        if self.fire_timer > 0:
            self.fire_timer -= 1


class Door:
    def __init__(self, x, y):
        self.x, self.y = x * CELL_WIDTH, y * CELL_HEIGHT
        self.open = False

    def draw(self, surf):
        if self.open:
            surf.blit(TEXTURES[6][1], (self.x, self.y))
        else:
            surf.blit(TEXTURES[5][1], (self.x, self.y))


class Monstr:
    def __init__(self, x, y, t=0):
        self.x, self.y = x * CELL_WIDTH, y * CELL_HEIGHT
        self.anim_pos = 0
        self.sleep = False
        self.sleep_timer = 0
        self.dir = None
        self.last_tile = None
        self.AI_type = t
        self.path = []
        self.point = None

    def go_sleep(self):
        self.sleep = True
        self.sleep_timer = 300

    def draw(self, surf):
        if not self.sleep:
            surf.blit(TEXTURES[ANIMATIONS[8][floor(self.anim_pos)]][1], (self.x, self.y))
            self.anim_pos += 0.01
            self.anim_pos %= len(ANIMATIONS[8])
        else:
            surf.blit(TEXTURES[24][1], (self.x, self.y))

        if self.sleep:
            self.sleep_timer -= 1
            if self.sleep_timer == 0:
                self.sleep = False

    def move(self, dx, dy):
        if self.AI_type == 0:
            my_rect = pg.Rect((self.x + 5 + dx, self.y + 15 + dy, CELL_WIDTH - 5, CELL_HEIGHT - 15))

            for i in map_now:
                if i[0] == TEXTURES[1][1]:
                    other_rect = pg.Rect((i[1][0], i[1][1], CELL_WIDTH, CELL_HEIGHT))

                    # noinspection PyTypeChecker
                    if rect_rect_intersect(my_rect, other_rect):
                        if not dx == 0:
                            dx = 0

                        if not dy == 0:
                            dy = 0

        self.x += dx * (PLAYER_SPEED + 0.05)
        self.y += dy * (PLAYER_SPEED + 0.05)

        # self.x, self.y = round(self.x), round(self.y)

    def is_on_floor(self):
        d = self.dir[0] * (CELL_WIDTH / 2.4) if self.dir else 0
        my_rect = pg.Rect((self.x + CELL_WIDTH/2 - d, self.y + CELL_HEIGHT, 2, 1))

        for i in map_now:
            if i[0] == TEXTURES[1][1]:
                other_rect = pg.Rect((i[1][0], i[1][1], CELL_WIDTH, CELL_HEIGHT))

                # noinspection PyTypeChecker
                if rect_rect_intersect(my_rect, other_rect):
                    return True

        return False

    def is_on_stairs(self):
        d = self.dir[0] * (CELL_WIDTH / 3) if self.dir else 0
        my_rect1 = pg.Rect((self.x + CELL_WIDTH/2 - d, self.y + CELL_HEIGHT / 2, 1, 1))
        my_rect2 = pg.Rect((self.x + CELL_WIDTH/2 - d, self.y + CELL_HEIGHT, 1, 1))

        for i in map_now:
            if i[0] == TEXTURES[2][1]:
                other_rect = pg.Rect((i[1][0], i[1][1], CELL_WIDTH, CELL_HEIGHT))

                # noinspection PyTypeChecker
                if rect_rect_intersect(my_rect1, other_rect) or rect_rect_intersect(my_rect2, other_rect):
                    return True

        return False

    def reload_dir(self):
        x, y = round(self.x / CELL_WIDTH), round(self.y / CELL_HEIGHT) * MAP_SIZE[0]
        left_tile = map_now[x-1+y]
        up_tile = map_now[x+y-MAP_SIZE[0]]
        right_tile = map_now[x+1+y]
        down_tile = map_now[x+y+MAP_SIZE[0]]

        dirs = []

        if not self.is_on_floor() and not self.is_on_stairs():
            self.dir = [0, 1]
            return
        else:
            if self.dir:
                if self.dir == [-1, 0]:
                    for i in range(50):
                        dirs.append(0)
                if self.dir == [0, 1]:
                    for i in range(50):
                        dirs.append(1)
                if self.dir == [1, 0]:
                    for i in range(50):
                        dirs.append(2)
                if self.dir == [0, -1]:
                    for i in range(50):
                        dirs.append(3)
            if left_tile[0] == TEXTURES[0][1] or left_tile[0] == TEXTURES[2][1]:
                dirs.append(0)
            if up_tile[0] == TEXTURES[2][1]:
                dirs.append(1)
            if right_tile[0] == TEXTURES[0][1] or right_tile[0] == TEXTURES[2][1]:
                dirs.append(2)
            if down_tile[0] == TEXTURES[2][1]:
                dirs.append(3)

        if len(dirs) > 0:
            new_dir = dirs[randint(0, len(dirs)-1)]

            if new_dir == 0:
                self.dir = [-1, 0]
            if new_dir == 1:
                self.dir = [0, -1]
            if new_dir == 2:
                self.dir = [1, 0]
            if new_dir == 3:
                self.dir = [0, 1]

    def think(self, player, graph):
        if self.sleep:
            return

        if self.AI_type == 0:
            pass

        if self.AI_type == 1:
            self.path_move()

            player_x, player_y = round(player.x / CELL_WIDTH), round(player.y / CELL_HEIGHT)
            x, y = round(self.x / CELL_WIDTH), round(self.y / CELL_HEIGHT)

            self.path = graph.path(x+y*MAP_SIZE[0], player_x+player_y*MAP_SIZE[0])
            #print(self.path, self.x, self.y, self.point)

            if not self.point and self.path:
                self.point = map_now[self.path[0]][1]

    def path_move(self):
        if self.path and len(self.path) > 1:
            dx, dy = self.point[0] - self.x, self.point[1] - self.y
            if (dx ** 2 + dy ** 2) ** 0.5 <= 5:
                self.point = map_now[self.path[1]][1]

            dx, dy = self.point[0] - 0.5 - self.x, self.point[1] - self.y

            if abs(dx) > 0:
                dx /= abs(dx)

            if abs(dy) > 0:
                dy /= abs(dy)

            dx, dy = round(dx), round(dy)

            #print(dx, dy)

            self.move(dx, dy)

class Bullet:
    def __init__(self, x, y, d):
        self.x, self.y, self.dir = x, y, d
        self.image = pg.image.load("textures/bullet.bmp")

    def check_collision(self, objects):
        my_rect = pg.Rect((self.x + 5, self.y + 2, 8, 4))

        for i in objects:
            other_rect = pg.Rect((i.x, i.y, CELL_WIDTH, CELL_HEIGHT))

            # noinspection PyTypeChecker
            if rect_rect_intersect(my_rect, other_rect):
                if isinstance(i, Monstr):
                    return i

        for i in map_now:
            if i[0] == TEXTURES[1][1]:
                other_rect = pg.Rect((i[1][0], i[1][1], CELL_WIDTH, CELL_HEIGHT))

                # noinspection PyTypeChecker
                if rect_rect_intersect(my_rect, other_rect):
                    return "block"

    def draw(self, surf):
        self.x += self.dir
        surf.blit(self.image, (self.x, self.y))
