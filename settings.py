import pygame as pg

# 處理座標、移動
vec = pg.math.Vector2

# 每秒幀數
FPS = 60
FIELD_COLOR = (55, 55, 55)
BG_COLOR = (162, 169, 179)
SHADOW_COLOR = (100, 100, 100)

# 字體
FONT_PATH = 'dutch-coffee/Regular.otf'

# 動畫時間間隔
ANIM_TIME_INTERVAL = 400  # 毫秒
FAST_ANIM_TIME_INTERVAL = 10

TILE_SIZE = 35  # 磚塊大小
FIELD_SIZE = FIELD_W, FIELD_H = 10, 20  # 遊戲區域尺寸
FIELD_RES = FIELD_W * TILE_SIZE, FIELD_H * TILE_SIZE  # 遊戲場地解析度

FIELD_SCALE_W, FIELD_SCALE_H = 2, 1  # 縮放比例
WIN_RES = WIN_W, WIN_H = FIELD_RES[0] * FIELD_SCALE_W, FIELD_RES[1] * FIELD_SCALE_H  # 視窗解析度

# 位置偏移量
INIT_POS_OFFSET = vec(FIELD_W // 2 - 1, 0)
NEXT_POS_OFFSET = vec(FIELD_W * 1.48, FIELD_H * 0.615)

# 控制方塊移動方向
MOVE_DIRECTIONS = {'left': vec(-1, 0), 'right': vec(1, 0), 'down': vec(0, 1)}

# 方塊樣式與顏色
TETROMINOES = {
    'T': {'blocks' : [(0, 0), (-1, 0), (1, 0), (0, -1)], 'color' : 'mediumorchid1'}, 
    'O': {'blocks' : [(0, 0), (0, -1), (1, 0), (1, -1)], 'color' : 'yellow2'}, 
    'J': {'blocks' : [(0, 0), (0, -1), (0, 1), (-1, 1)], 'color' : 'dodgerblue4'},
    'L': {'blocks' : [(0, 0), (0, 1), (1, 1), (0, -1)], 'color' : 'darkorange2'},
    'I': {'blocks' : [(0, 0), (0, 1), (0, -1), (0, -2)], 'color' : 'deepskyblue'},
    'S': {'blocks' : [(0, 0),(-1, 0), (0, -1), (1, -1)], 'color' : 'darkred'},
    'Z': {'blocks' : [(0, 0), (1, 0), (0, -1), (-1, -1)], 'color' : 'lawngreen'}
}
