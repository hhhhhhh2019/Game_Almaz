RES = WIDTH, HEIGHT = 1280, 1020
CAPTION =  "Almaz"
FPS = 60
MAP_SIZE = [15, 10]
CELL_WIDTH, CELL_HEIGHT = WIDTH // MAP_SIZE[0], HEIGHT // MAP_SIZE[1]
MAP = 0
map_now = []
PLAYER_SPEED = 1
DIAMONDS = 0
bullets = []

player = None
graph = None

TEXTURES = [
    ["textures/oldkirpich.bmp", None], # 0 фон
    ["textures/kirpich.bmp", None], # 1 стена
    ["textures/lestnica.bmp", None], # 2 лестница
    ["textures/path_kirpich.bmp", None], # 3 фон для пути
    #["textures/d_path_kirpich.bmp", None], # 4 фон для пути
    ["textures/oldkirpich.bmp", None], # 4 фон для пути
    ["textures/door1.bmp", None], # 5 закрытая дверь
    ["textures/door2.bmp", None], # 6 открытая дверь
    ["textures/aniall-14.png", None], # 7 алмаз
    ["textures/aniall-15.png", None], # 8 алмаз
    ["textures/aniall-16.png", None], # 9 алмаз
    ["textures/aniall-17.png", None], # 10 игрок
    ["textures/aniall-3.png", None], # 11 игрок
    ["textures/aniall-4.png", None], # 12 игрок
    ["textures/aniall-5.png", None], # 13 игрок
    ["textures/aniall-6.png", None], # 14 игрок
    ["textures/aniall-7.png", None], # 15 игрок
    ["textures/aniall-8.png", None], # 16 игрок
    ["textures/aniall-9.png", None], # 17 игрок
    ["textures/aniall-10.png", None], # 18 игрок
    ["textures/aniall-11.png", None], # 19 игрок
    ["textures/aniall-12.png", None], # 20 игрок
    ["textures/aniall-13.png", None], # 21 игрок
    ["textures/aniall-0.png", None], # 22 монстр
    ["textures/aniall-1.png", None], # 23 монстр
    ["textures/aniall-2.png", None], # 24 монстр
    ["textures/ded2.bmp", None, RES], # 25 экран смерти
    ["textures/level.bmp", None, RES], # 26 экран победы
]

OBJECTS = {
    "block": TEXTURES[1][0],
    "empty": TEXTURES[0][0],
    "stairs": TEXTURES[2][0],
    "fall": TEXTURES[4][0]
}

ANIMATIONS = [
    [7, 8, 9, 8], # 0 вращение алмаза
    [10], # 1 игрок-покой
    [13, 16], # 2 игрок-хотьба влево
    [14, 15], # 3 игрок-хотьба вправо
    [17, 18], # 4 игрок-поднимание вверх
    [19], # 5 игрок-стрельба влево
    [20], # 6 игрок-стрельба вправо
    [21], # 7 игрок падение
    [23, 22, 23], # 8 монстр не заморожен
    [24], # 9 монстр заморожен
]