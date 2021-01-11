from maps import *
from objects import *
from Graph import *
pg.init()
# import pygame as pg

full_screen = True

screen = None

if full_screen:
    screen = pg.display.set_mode(RES, pg.FULLSCREEN)
else:
    screen = pg.display.set_mode(RES)
pg.display.set_caption(CAPTION)
clock = pg.time.Clock()

objects = []
door = None

keys = []

run = False
pause = False

def load_textures():
    print("загрузка текстур")
    for i in TEXTURES:
        print("\t" + i[0])
        w, h = CELL_WIDTH, CELL_HEIGHT
        try:
            w, h = i[2]
        except:
            pass
        surf = pg.transform.scale(pg.image.load(i[0]), (w, h))
        i[1] = surf


def load_map():
    global graph, objects, player, door, DIAMONDS#, left_tile, up_tile, right_tile, down_tile, down_left_tile, down_right_tile
    DIAMONDS = len(MAPS[MAP][3])
    player = Player(*MAPS[MAP][0])

    objects = []
    [objects.append(Almaz(p[0], p[1])) for p in MAPS[MAP][3]]
    [objects.append(Monstr(p[0], p[1], p[2])) for p in MAPS[MAP][4]]
    objects.append(Door(*MAPS[MAP][1]))

    for i in range(len(MAPS[MAP][2])):
        x = (i % MAP_SIZE[0]) * CELL_WIDTH
        y = (i // MAP_SIZE[0]) * CELL_HEIGHT
        map_now.append([TEXTURES[MAPS[MAP][2][i]][1], (x, y), TEXTURES[MAPS[MAP][2][i]][0]])

    bullets.clear()

    g = {}

    for i in map_now:
        p = []

        x, y = round(i[1][0] / CELL_WIDTH), round(i[1][1] / CELL_HEIGHT)
        my_tile = i[2]

        if not my_tile == OBJECTS["block"]:
            left_x, left_y = round(i[1][0] / CELL_WIDTH - 1), round(i[1][1] / CELL_HEIGHT)
            left_tile = map_now[left_x + left_y * MAP_SIZE[0]][2]

            right_x, right_y = round(i[1][0] / CELL_WIDTH  + 1), round(i[1][1] / CELL_HEIGHT)
            right_tile = map_now[right_x + right_y * MAP_SIZE[0]][2]

            up_x, up_y = round(i[1][0] / CELL_WIDTH), round(i[1][1] / CELL_HEIGHT - 1)
            up_tile = map_now[up_x + up_y * MAP_SIZE[0]][2]

            down_x, down_y = round(i[1][0] / CELL_WIDTH), round(i[1][1] / CELL_HEIGHT + 1)
            down_tile = map_now[down_x + down_y * MAP_SIZE[0]][2]

            if down_tile == OBJECTS["block"] or down_tile == OBJECTS["stairs"]:
                if not left_tile == OBJECTS["block"]:
                    p.append(left_x + left_y * MAP_SIZE[0])

                if not right_tile == OBJECTS["block"] or right_x + right_y * 15 == 125:
                    p.append(right_x + right_y * MAP_SIZE[0])

                if up_tile == OBJECTS["stairs"] and my_tile == OBJECTS["stairs"] or\
                        up_tile == OBJECTS["empty"] and my_tile == OBJECTS["stairs"]:
                    p.append(up_x + up_y * MAP_SIZE[0])

                if down_tile == OBJECTS["stairs"] or down_tile == OBJECTS["empty"]:
                    p.append(down_x + down_y * MAP_SIZE[0])

            if my_tile == OBJECTS["fall"] and not down_tile == OBJECTS["block"]:
                p.append(down_x + down_y * MAP_SIZE[0])


        g[x + y * MAP_SIZE[0]] = p

    graph = BFS(g)

def ded():
    pause = True
    screen.blit(TEXTURES[25][1], (0, 0))
    pg.display.flip()
    pg.time.delay(5000)
    load_map()
    pause = False

def win():
    global MAP
    pause = True
    screen.blit(TEXTURES[26][1], (0, 0))
    pg.display.flip()
    MAP += 1
    MAP %= len(MAPS)
    map_now.clear()
    pg.time.delay(5000)
    load_map()
    pause = False

def start():
    global DIAMONDS, MAP, run, full_screen, screen
    run = True
    while run and not pause:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                exit()

            if e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    exit()

                if e.key == pg.K_F11:
                    full_screen = not full_screen
                    if full_screen:
                        screen = pg.display.set_mode(RES, pg.FULLSCREEN)
                    else:
                        screen = pg.display.set_mode(RES)

                if e.key == pg.K_F5:
                    ded()

                if e.key == pg.K_LEFT:
                    keys.append("left")
                if e.key == pg.K_RIGHT:
                    keys.append("right")
                if e.key == pg.K_UP:
                    keys.append("up")
                if e.key == pg.K_DOWN:
                    keys.append("down")
                if e.key == pg.K_z:
                    keys.append("fire_left")
                if e.key == pg.K_x:
                    keys.append("fire_right")

            if e.type == pg.KEYUP:
                if e.key == pg.K_LEFT and "left" in keys:
                    keys.remove("left")
                if e.key == pg.K_RIGHT and "right" in keys:
                    keys.remove("right")
                if e.key == pg.K_UP and "up" in keys:
                    keys.remove("up")
                if e.key == pg.K_DOWN and "down" in keys:
                    keys.remove("down")
                if e.key == pg.K_z and "fire_left" in keys:
                    keys.remove("fire_left")
                if e.key == pg.K_x and "fire_right" in keys:
                    keys.remove("fire_right")

        for i in map_now:
            screen.blit(i[0], i[1])

        for i in bullets:
            a = i.check_collision(objects)
            if a:
                bullets.remove(i)
                if isinstance(a, Monstr):
                    a.go_sleep()
            else:
                i.draw(screen)

        for i in objects:
            if isinstance(i, Monstr):
                i.think(player, graph)
            i.draw(screen)

        player.control(keys)
        a = player.check_collision(objects)
        if isinstance(a, Almaz):
            DIAMONDS -= 1
            objects.remove(a)
            if DIAMONDS == 0:
                objects[-1].open = True
        elif isinstance(a, Door):
            if a.open:
                win()
        elif isinstance(a, Monstr) and not a.sleep:
            ded()
        player.draw(screen)

        pg.display.flip()
        clock.tick(FPS)

        # pg.display.set_caption(str(clock.get_fps()))

load_textures()
load_map()

#print(graph.graph)

start()