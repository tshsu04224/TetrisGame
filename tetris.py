from settings import *
from tetromino import Tetromino
import pygame.freetype as ft  # 字型模組

class Text:
    def __init__(self, app):
        self.app = app
        self.font = ft.Font(FONT_PATH)  # 字體

    # 繪製文字
    def draw(self):
        self.font.render_to(self.app.screen, (WIN_W * 0.595, WIN_H * 0.02),
                            text='TETRIS', fgcolor='white',
                            size=TILE_SIZE * 1.75, bgcolor='black')
        self.font.render_to(self.app.screen, (WIN_W * 0.675, WIN_H * 0.125),
                            text='HOLD', fgcolor='orange',
                            size=TILE_SIZE * 1.3, bgcolor='black')
        self.font.render_to(self.app.screen, (WIN_W * 0.675, WIN_H * 0.425),
                            text='NEXT', fgcolor='orange',
                            size=TILE_SIZE * 1.3, bgcolor='black')
        self.font.render_to(self.app.screen, (WIN_W * 0.665, WIN_H * 0.75),
                            text='SCORE', fgcolor='yellow',
                            size=TILE_SIZE * 1.3, bgcolor='black')
        # 繪製分數
        score_text = f'{self.app.tetris.score}'
        score_rect = self.font.get_rect(score_text, size=TILE_SIZE * 1.7)
        score_x = WIN_W * 0.76 - (score_rect.width / 2)
        score_y = WIN_H * 0.85
        self.font.render_to(self.app.screen, (score_x, score_y),
                            text=score_text, fgcolor='white',
                            size=TILE_SIZE * 1.7)

class Tetris:
    def __init__(self, app):
        self.app = app
        self.sprite_group = pg.sprite.Group()
        self.field_array = self.get_field_array()
        self.tetromino = Tetromino(self)
        self.next_tetromino = Tetromino(self, current=False)
        self.speed_up = False
        self.hold_used = False
        self.hold_tetromino = None

        # 分數
        self.score = 0
        self.full_lines = 0
        self.points_per_lines = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

        # 移動延遲、加速
        self.base_move_delay = 500
        self.move_delay = self.base_move_delay
        self.move_acceleration = 150  # 移動加速度
        self.last_move_time = pg.time.get_ticks()
        self.last_key_time = pg.time.get_ticks()

    # 暫存
    def hold_current_tetromino(self):
        if not self.hold_used:
            if self.hold_tetromino is None:
                self.tetromino.reset_position()
                self.hold_tetromino = self.tetromino
                self.tetromino = self.next_tetromino
                self.next_tetromino = Tetromino(self, current=False)
            else:
                self.tetromino.reset_position()
                self.hold_tetromino, self.tetromino = self.tetromino, self.hold_tetromino
            self.tetromino.reset_position()
            self.hold_used = True

    # 計算得分
    def get_score(self):
        self.score += self.points_per_lines[self.full_lines]
        self.full_lines = 0


    def check_full_lines(self):
        row = FIELD_H - 1
        for y in range(FIELD_H - 1, -1, -1):
            for x in range(FIELD_W):
                self.field_array[row][x] = self.field_array[y][x]
                if self.field_array[y][x]:
                    self.field_array[row][x].pos = vec(x, y)
            if sum(map(bool, self.field_array[y])) < FIELD_W:
                row -= 1
            else:
                for x in range(FIELD_W):
                    self.field_array[row][x].alive = False
                    self.field_array[row][x] = 0
                self.full_lines += 1

    # 將當前方塊放入陣列
    def put_tetromino_blocks_in_array(self):
        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            if 0 <= x < FIELD_W and 0 <= y < FIELD_H:
                self.field_array[y][x] = block

    # 初始化遊戲場地陣列
    def get_field_array(self):
        return [[0 for x in range(FIELD_W)] for y in range(FIELD_H)]


    def is_game_over(self):
        if self.tetromino.blocks[0].pos.y == INIT_POS_OFFSET[1]:
            pg.time.wait(300)
            self.app.game_over = True
            return True

    # 檢查方塊是否著陸
    def check_tetromino_landing(self):
        if self.tetromino.landing:
            if self.is_game_over():
                # self.__init__(self.app)
                return
            else:
                self.speed_up = False
                self.put_tetromino_blocks_in_array()
                self.next_tetromino.current = True
                self.tetromino = self.next_tetromino
                self.next_tetromino = Tetromino(self, current=False)
                self.move_delay = self.base_move_delay
                self.hold_used = False

    # 控制方塊移動
    def control(self, pressed_keys):
        if pressed_keys == pg.K_LEFT:
            self.tetromino.move(direction='left')
            self.move_delay -= self.move_acceleration
        elif pressed_keys == pg.K_RIGHT:
            self.tetromino.move(direction='right')
            self.move_delay -= self.move_acceleration
        elif pressed_keys == pg.K_DOWN:
            self.tetromino.move(direction='down')
            self.move_delay -= self.move_acceleration
        elif pressed_keys == pg.K_UP:
            self.tetromino.rotate()
        elif pressed_keys == pg.K_LCTRL:
            while not self.tetromino.landing:
                self.tetromino.move(direction='down')
            self.speed_up = True
        elif pressed_keys == pg.K_LSHIFT:
            self.hold_current_tetromino()

    # 更新遊戲狀態
    def update(self, pressed_keys):
        current_time = pg.time.get_ticks()

        if current_time - self.last_key_time > self.move_delay:
            if pg.K_LEFT in pressed_keys or pg.K_RIGHT in pressed_keys or pg.K_DOWN in pressed_keys:
                self.last_key_time = current_time

        trigger = [self.app.anim_trigger, self.app.fast_anim_trigger][self.speed_up]
        if trigger:
            self.check_full_lines()
            self.tetromino.update()
            self.check_tetromino_landing()
            self.get_score()
        self.sprite_group.update()

        if current_time - self.last_move_time > self.move_delay:
            if pg.K_LEFT in pressed_keys:
                self.tetromino.move(direction='left')
                self.move_delay -= self.move_acceleration
            elif pg.K_RIGHT in pressed_keys:
                self.tetromino.move(direction='right')
                self.move_delay -= self.move_acceleration
            elif pg.K_DOWN in pressed_keys:
                self.tetromino.move(direction='down')
                self.move_delay -= self.move_acceleration
            if pg.KEYUP:
                self.last_move_time = current_time


    def draw_grid(self):
        for x in range(FIELD_W):
            for y in range(FIELD_H):
                pg.draw.rect(self.app.screen, 'gray3',
                             (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

    # 繪製遊戲內容
    def draw(self):
        self.draw_grid()
        self.draw_hold_box()
        self.draw_hold()
        self.draw_shadow()
        self.sprite_group.draw(self.app.screen)

    # 繪製 hold 區域中的方塊
    def draw_hold(self):
        if self.hold_tetromino:
            hold_box_x = WIN_W * 0.48
            hold_box_y = WIN_H * 0.255
            for block in self.hold_tetromino.blocks:
                block.set_rect_pos()
                block.rect.topleft = (hold_box_x + (block.pos.x + 1) * TILE_SIZE,
                                      hold_box_y + (block.pos.y + 1) * TILE_SIZE)
                self.app.screen.blit(block.image, block.rect.topleft)

    # 繪製 hold 方框
    def draw_hold_box(self):
        hold_box_x = WIN_W * 0.65
        hold_box_y = WIN_H * 0.2
        hold_box_width = TILE_SIZE * 4 + 8
        hold_box_height = TILE_SIZE * 4 + 8
        pg.draw.rect(self.app.screen, (55, 55, 55), (hold_box_x, hold_box_y, hold_box_width, hold_box_height))
        pg.draw.rect(self.app.screen, (0, 0, 0), (hold_box_x, hold_box_y, hold_box_width, hold_box_height), 3)

    # 繪製方塊影子
    def draw_shadow(self):
        shadow_blocks = self.tetromino.get_shadow_blocks()
        for block_pos in shadow_blocks:
            rect = pg.Rect(block_pos.x * TILE_SIZE, block_pos.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pg.draw.rect(self.app.screen, SHADOW_COLOR, rect)
            pg.draw.rect(self.app.screen, 'white', rect, 1)

    # 獲取影子方塊的位置
    def get_shadow_blocks(self):
        shadow_tetromino = self.tetromino.copy()
        while not shadow_tetromino.landing:
            shadow_tetromino.move(direction='down')
        return [block.pos for block in shadow_tetromino.blocks]
