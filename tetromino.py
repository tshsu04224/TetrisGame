import random
import pygame as pg
from settings import *

class Block(pg.sprite.Sprite):
    def __init__(self, tetromino, pos):
        self.tetromino = tetromino
        self.pos = pg.math.Vector2(pos) + INIT_POS_OFFSET
        self.initial_pos = self.pos
        self.next_pos = pg.math.Vector2(pos) + NEXT_POS_OFFSET
        self.alive = True

        super().__init__(tetromino.tetris.sprite_group)
        self.image = pg.Surface([TILE_SIZE, TILE_SIZE])
        color = TETROMINOES[tetromino.shape]['color']
        # 繪製方塊圖像
        pg.draw.rect(self.image, color, (1, 1, TILE_SIZE - 2, TILE_SIZE - 2), border_radius=8)
        self.rect = self.image.get_rect()

        # 設定方塊特效
        self.sfx_image = self.image.copy()
        self.sfx_image.set_alpha(110)
        self.sfx_speed = random.uniform(0.2, 0.6)
        self.sfx_cycles = random.randrange(6, 8)
        self.cycle_counter = 0

    # 設置方塊的矩形位置
    def set_rect_pos(self):
        pos = [self.next_pos, self.pos][self.tetromino.current]
        self.rect.topleft = pos * TILE_SIZE

    # 判斷方塊特效是否結束
    def sfx_end_time(self):
        if self.tetromino.tetris.app.anim_trigger:
            self.cycle_counter += 1
            if self.cycle_counter > self.sfx_cycles:
                self.cycle_counter = 0
                return True

    # 執行方塊特效
    def sfx_run(self):
        self.image = self.sfx_image
        self.pos.y -= self.sfx_speed
        self.image = pg.transform.rotate(self.image, pg.time.get_ticks() * self.sfx_speed)


    def is_alive(self):
        if not self.alive:
            if not self.sfx_end_time():
                self.sfx_run()
            else:
                self.kill()

    # 旋轉
    def rotate(self, pivot_pos):
        translated = self.pos - pivot_pos
        rotated = translated.rotate(90)
        return rotated + pivot_pos

    # 更新方塊狀態
    def update(self):
        self.set_rect_pos()
        self.is_alive()

    # 檢查方塊是否與其他方塊或遊戲邊界碰撞
    def is_collide(self, pos):
        x, y = int(pos.x), int(pos.y)
        if 0 <= x < FIELD_W and y < FIELD_H and (
                y < 0 or not self.tetromino.tetris.field_array[y][x]):
            return False
        return True


class Tetromino:
    def __init__(self, tetris, current=True):
        self.tetris = tetris
        self.shape = random.choice(list(TETROMINOES.keys()))
        self.blocks = [Block(self, pos) for pos in TETROMINOES[self.shape]['blocks']]
        self.landing = False
        self.current = current

    # 重置方塊組合位置
    def reset_position(self):
        for block in self.blocks:
            block.kill()
        self.blocks = [Block(self, pos) for pos in TETROMINOES[self.shape]['blocks']]
        self.landing = False
        self.current = True


    def rotate(self):
        pivot_pos = self.blocks[0].pos
        new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]

        if not self.is_collide(new_block_positions):
            for i, block in enumerate(self.blocks):
                block.pos = new_block_positions[i]


    def is_collide(self, block_positions):
        for pos in block_positions:
            x, y = int(pos.x), int(pos.y)
            if x < 0 or x >= FIELD_W or y >= FIELD_H or (y >= 0 and self.tetris.field_array[y][x]):
                return True
        return False

    # 移動方塊組合
    def move(self, direction):
        move_direction = MOVE_DIRECTIONS[direction]
        new_block_positions = [block.pos + move_direction for block in self.blocks]
        is_collide = self.is_collide(new_block_positions)

        if not is_collide:
            for block in self.blocks:
                block.pos += move_direction

        elif direction == 'down':
            self.landing = True


    def update(self):
        self.move(direction='down')

    # 獲取方塊組合的影子位置
    def get_shadow_blocks(self):
        shadow_blocks = [vec(block.pos) for block in self.blocks]
        while True:
            new_block_positions = [pos + vec(0, 1) for pos in shadow_blocks]
            if self.is_collide(new_block_positions):
                break
            shadow_blocks = new_block_positions
        return shadow_blocks
