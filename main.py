from settings import *
from tetris import Tetris, Text
import sys

class App:
    def __init__(self):
        pg.init()

        # 音樂
        pg.mixer.init()
        pg.mixer.music.load('tetris-battle-music.mp3')
        pg.mixer.music.play(-1)

        pg.display.set_caption('Tetris')
        self.screen = pg.display.set_mode(WIN_RES)
        self.clock = pg.time.Clock()
        self.set_timer()
        self.tetris = Tetris(self)
        self.text = Text(self)
        self.pressed_keys = set()
        self.game_over = False
        self.restart_button = None


    def set_timer(self):
        self.user_event = pg.USEREVENT + 0
        self.fast_user_event = pg.USEREVENT + 1
        self.anim_trigger = False
        self.fast_anim_trigger = False
        pg.time.set_timer(self.user_event, ANIM_TIME_INTERVAL)
        pg.time.set_timer(self.fast_user_event, FAST_ANIM_TIME_INTERVAL)


    def update(self):
        if not self.game_over:
            self.tetris.update(self.pressed_keys)
        self.clock.tick(FPS)  # 控制遊戲幀率

    # 繪製遊戲畫面
    def draw(self):
        self.screen.fill(color=BG_COLOR)
        self.screen.fill(color=FIELD_COLOR, rect=(0, 0, *FIELD_RES))
        self.tetris.draw()
        self.text.draw()
        if self.game_over:
            self.draw_game_over()
        pg.display.flip()


    def check_events(self):
        self.anim_trigger = False
        self.fast_anim_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):  # Esc 鍵: 退出遊戲 
                pg.quit()
                sys.exit()

            elif event.type == pg.KEYDOWN:
                if not self.game_over:
                    if event.key == pg.K_LSHIFT:  # 左 Shift 鍵: 方塊暫存
                        self.tetris.hold_current_tetromino()
                    else:    
                        self.pressed_keys.add(event.key)
                        self.tetris.control(event.key)

            elif event.type == pg.KEYUP:
                if event.key in self.pressed_keys:
                    self.pressed_keys.remove(event.key)
                    # 放開左右移動鍵，重置move_delay
                    if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                        self.tetris.move_delay = self.tetris.base_move_delay     

            elif event.type == self.user_event:
                self.anim_trigger = True
            elif event.type == self.fast_user_event:
                self.fast_anim_trigger = True

            elif event.type == pg.MOUSEBUTTONDOWN and self.game_over:
                if self.restart_button.collidepoint(event.pos):
                    self.restart_game()


    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()
            self.update_cursor()

    # game over畫面
    def draw_game_over(self):
        overlay = pg.Surface((WIN_W, WIN_H))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(180)
        self.screen.blit(overlay, (0, 0))

        font = pg.font.Font(FONT_PATH, TILE_SIZE)
        game_over_text = font.render("GAME OVER", True, "red")
        score_text = font.render(f"SCORE {self.tetris.score}", True, "white")

        game_over_rect = game_over_text.get_rect(center=(WIN_W // 2, WIN_H // 2 - 70))
        score_rect = score_text.get_rect(center=(WIN_W // 2, WIN_H // 2))

        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)

        self.restart_button = pg.Rect(WIN_W // 2 - 100, WIN_H // 2 + 50, 200, 50)
        pg.draw.rect(self.screen, (0, 255, 0), self.restart_button)
        restart_text = font.render("Restart", True, "black")
        restart_rect = restart_text.get_rect(center=self.restart_button.center)
        self.screen.blit(restart_text, restart_rect)


    def restart_game(self):
        self.tetris = Tetris(self)
        self.game_over = False

    # restart 按鈕箭頭、手指
    def update_cursor(self):
        if self.game_over and self.restart_button:
            mouse_pos = pg.mouse.get_pos()
            if self.restart_button.collidepoint(mouse_pos):
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
            else:
                pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)

  

if __name__ == '__main__':
    app = App()
    app.run()
