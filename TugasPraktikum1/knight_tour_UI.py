import sys
import pygame
import knight_tour as engine

pygame.init()

# --- CONSTANTS & CONFIG ---
WIDTH, HEIGHT = 900, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Knight's Tour (Warnsdorff's Rule) - Optimization")

# --- PALET WARNA ---
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
TEXT_COLOR = (30, 30, 30)

# Warna Papan
BOARD_LIGHT = (240, 217, 181)  
BOARD_DARK  = (181, 136, 99)   

# Warna State
COLOR_VISITED = (241, 196, 15) 
COLOR_START   = (52, 152, 219) 
COLOR_HEAD    = (231, 76, 60)  
COLOR_LINE    = (80, 80, 80)    
COLOR_LAST_MOVE = (255, 0, 0)   

# UI Colors
BTN_BLUE  = (41, 128, 185)
BTN_RED   = (192, 57, 43)
BTN_GREEN = (39, 174, 96)
PANEL_BG  = (236, 240, 241)

# Fonts
FONT_H1 = pygame.font.SysFont("segoeui", 32, bold=True)
FONT_CELL = pygame.font.SysFont("segoeui", 22, bold=True)
FONT_TEXT = pygame.font.SysFont("segoeui", 16)
FONT_BTN = pygame.font.SysFont("segoeui", 16, bold=True)

# Grid Layout
BOARD_SIZE = 8
CELL_SIZE = 60
GRID_X0, GRID_Y0 = 50, 60 

# --- UI COMPONENTS ---
class Button:
    def __init__(self, rect, text, bg=BTN_BLUE, fg=WHITE, callback=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.bg = bg
        self.fg = fg
        self.callback = callback
        self.hover = False

    def draw(self, surf):
        color = tuple(min(255, c+30) for c in self.bg) if self.hover else self.bg
        pygame.draw.rect(surf, (0,0,0,50), (self.rect.x+2, self.rect.y+3, self.rect.w, self.rect.h), border_radius=8)
        pygame.draw.rect(surf, color, self.rect, border_radius=8)
        pygame.draw.rect(surf, (255,255,255, 50), self.rect, width=1, border_radius=8)
        label = FONT_BTN.render(self.text, True, self.fg)
        surf.blit(label, label.get_rect(center=self.rect.center))

    def handle(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.callback:
                self.callback()

class Dropdown:
    def __init__(self, rect, options, default_idx=0):
        self.rect = pygame.Rect(rect)
        self.options = options
        self.index = default_idx
        self.open = False
        self.bg_color = WHITE

    def value(self):
        return self.options[self.index]

    def draw(self, surf):
        pygame.draw.rect(surf, self.bg_color, self.rect, border_radius=6)
        pygame.draw.rect(surf, (100,100,100), self.rect, width=1, border_radius=6)
        text_val = self.value()
        label = FONT_BTN.render(str(text_val), True, TEXT_COLOR)
        surf.blit(label, (self.rect.x+10, self.rect.y+8))
        pygame.draw.polygon(surf, TEXT_COLOR, [(self.rect.right-20, self.rect.y+14),
                                             (self.rect.right-10, self.rect.y+14),
                                             (self.rect.right-15, self.rect.y+22)])
        if self.open:
            h = self.rect.height
            for i, opt in enumerate(self.options):
                r = pygame.Rect(self.rect.x, self.rect.y + (i+1)*h, self.rect.width, h)
                pygame.draw.rect(surf, WHITE, r)
                pygame.draw.rect(surf, (200,200,200), r, 1)
                lbl = FONT_BTN.render(str(opt), True, TEXT_COLOR)
                surf.blit(lbl, (r.x+10, r.y+8))

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.open = not self.open
            elif self.open:
                h = self.rect.height
                for i, _ in enumerate(self.options):
                    r = pygame.Rect(self.rect.x, self.rect.y + (i+1)*h, self.rect.width, h)
                    if r.collidepoint(event.pos):
                        self.index = i
                        self.open = False
                        break
                else:
                    self.open = False

# --- MAIN GAME CLASS ---
class Game:
    def __init__(self):
        self.logic = engine.KnightTourLogic(BOARD_SIZE)
        self.auto_play = False
        self.status_text = "Click board to Start"
        self.panel_x = 560
        
        y_controls = 480
        self.btn_reset = Button((self.panel_x, y_controls, 100, 40), "Reset", bg=BTN_RED, callback=self.reset_game)
        self.btn_play = Button((self.panel_x + 110, y_controls, 140, 40), "Play / Pause", bg=BTN_GREEN, callback=self.toggle_play)
        
        y_nav = 430
        self.btn_prev = Button((self.panel_x, y_nav, 70, 30), "< Prev", bg=BTN_BLUE, callback=self.prev_step)
        self.btn_next = Button((self.panel_x + 80, y_nav, 70, 30), "Next >", bg=BTN_BLUE, callback=self.next_step)
        self.btn_end = Button((self.panel_x + 160, y_nav, 90, 30), "End >>", bg=BTN_BLUE, callback=self.go_to_end)

        self.dd_speed = Dropdown((self.panel_x + 100, 380, 150, 35), ["Slow", "Normal", "Fast", "Instant"], default_idx=1)
        self.last_update = pygame.time.get_ticks()

    def reset_game(self):
        self.logic = engine.KnightTourLogic(BOARD_SIZE)
        self.auto_play = False
        self.status_text = "Board reset."

    def toggle_play(self):
        if self.logic.is_solved:
            self.auto_play = not self.auto_play

    def next_step(self):
        self.auto_play = False
        self.logic.next_step()

    def prev_step(self):
        self.auto_play = False
        self.logic.prev_step()
        
    def go_to_end(self):
        self.auto_play = False
        self.logic.go_to_end()

    def handle_click_board(self, pos):
        if self.logic.is_solved: return
        x, y = pos
        if GRID_X0 <= x < GRID_X0 + (BOARD_SIZE * CELL_SIZE) and \
           GRID_Y0 <= y < GRID_Y0 + (BOARD_SIZE * CELL_SIZE):
            col = (x - GRID_X0) // CELL_SIZE
            row = (y - GRID_Y0) // CELL_SIZE
            steps = self.logic.solve_tour(col, row)
            self.status_text = "Calculating..." 
            self.auto_play = True

    def update(self):
        if self.auto_play and self.logic.is_solved:
            speed_map = {"Slow": 500, "Normal": 150, "Fast": 30, "Instant": 1}
            delay = speed_map[self.dd_speed.value()]
            now = pygame.time.get_ticks()
            if now - self.last_update > delay:
                self.logic.next_step()
                self.last_update = now
                state = self.logic.get_current_state()
                if state["current_idx"] >= state["total_steps"] - 1:
                    self.auto_play = False
                    self.status_text = "Tour Finished!"

    def draw_grid(self):
        pygame.draw.rect(SCREEN, (0,0,0,50), (GRID_X0+5, GRID_Y0+5, BOARD_SIZE*CELL_SIZE, BOARD_SIZE*CELL_SIZE), border_radius=4)
        
        state = self.logic.get_current_state()
        path = state["path"]
        curr_idx = state["current_idx"]
        
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                x = GRID_X0 + c * CELL_SIZE
                y = GRID_Y0 + r * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                color = BOARD_LIGHT if (r+c)%2 == 0 else BOARD_DARK
                pygame.draw.rect(SCREEN, color, rect)

        if state["is_solved"]:
            for i in range(curr_idx + 1):
                cx, cy = path[i]
                x = GRID_X0 + cx * CELL_SIZE
                y = GRID_Y0 + cy * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                
                if i == 0:
                    pygame.draw.rect(SCREEN, COLOR_START, rect)
                elif i == curr_idx:
                    pygame.draw.rect(SCREEN, COLOR_HEAD, rect)
                else:
                    pygame.draw.rect(SCREEN, COLOR_VISITED, rect)
                
                pygame.draw.rect(SCREEN, (0,0,0), rect, 1)

            if curr_idx > 0:
                if curr_idx > 1:
                    old_points = []
                    for i in range(curr_idx):
                        cx, cy = path[i]
                        center_x = GRID_X0 + cx * CELL_SIZE + CELL_SIZE // 2
                        center_y = GRID_Y0 + cy * CELL_SIZE + CELL_SIZE // 2
                        old_points.append((center_x, center_y))
                    
                    if len(old_points) > 1:
                        pygame.draw.lines(SCREEN, COLOR_LINE, False, old_points, 3)

                prev_cx, prev_cy = path[curr_idx-1]
                p1 = (GRID_X0 + prev_cx * CELL_SIZE + CELL_SIZE // 2, 
                      GRID_Y0 + prev_cy * CELL_SIZE + CELL_SIZE // 2)
                
                cur_cx, cur_cy = path[curr_idx]
                p2 = (GRID_X0 + cur_cx * CELL_SIZE + CELL_SIZE // 2, 
                      GRID_Y0 + cur_cy * CELL_SIZE + CELL_SIZE // 2)
                
                pygame.draw.line(SCREEN, COLOR_LAST_MOVE, p1, p2, 5)


            for i in range(curr_idx + 1):
                cx, cy = path[i]
                center_x = GRID_X0 + cx * CELL_SIZE + CELL_SIZE // 2
                center_y = GRID_Y0 + cy * CELL_SIZE + CELL_SIZE // 2
                
                main_text_color = WHITE if (i == 0 or i == curr_idx) else BLACK
                
                txt = str(i+1)
                
                outline_color = BLACK if main_text_color == WHITE else WHITE
                
                for dx, dy in [(-1,-1), (-1,1), (1,-1), (1,1)]:
                    lbl_out = FONT_CELL.render(txt, True, outline_color)
                    out_rect = lbl_out.get_rect(center=(center_x+dx, center_y+dy))
                    SCREEN.blit(lbl_out, out_rect)
                
                lbl = FONT_CELL.render(txt, True, main_text_color)
                lbl_rect = lbl.get_rect(center=(center_x, center_y))
                SCREEN.blit(lbl, lbl_rect)

    def draw_panel(self):
        panel_rect = pygame.Rect(self.panel_x - 10, 50, 300, 500)
        pygame.draw.rect(SCREEN, PANEL_BG, panel_rect, border_radius=12)
        pygame.draw.rect(SCREEN, (200,200,200), panel_rect, width=1, border_radius=12)
        
        title = FONT_H1.render("Knight's Tour", True, BLACK)
        SCREEN.blit(title, (self.panel_x, 70))
        sub = FONT_TEXT.render("Warnsdorff's Rule Implementation", True, (100,100,100))
        SCREEN.blit(sub, (self.panel_x, 110))
        
        info_rect = pygame.Rect(self.panel_x, 150, 270, 180)
        pygame.draw.rect(SCREEN, WHITE, info_rect, border_radius=8)
        pygame.draw.rect(SCREEN, (220,220,220), info_rect, width=1, border_radius=8)
        
        state = self.logic.get_current_state()
        status_display = self.status_text
        if self.auto_play: status_display = "Animating..."
        
        lines = [
            ("Status", status_display),
            ("Total Steps", f"{state['total_steps']}"),
            ("Current Step", f"{state['current_idx'] + 1}"),
            ("Progress", f"{round((state['current_idx']+1)/64 * 100)}%")
        ]
        
        y_text = info_rect.y + 20
        for label, val in lines:
            lbl_surf = FONT_TEXT.render(label + ":", True, (100,100,100))
            val_surf = FONT_TEXT.render(val, True, BLACK)
            SCREEN.blit(lbl_surf, (info_rect.x + 15, y_text))
            SCREEN.blit(val_surf, (info_rect.x + 120, y_text))
            y_text += 35
            
        lbl_spd = FONT_BTN.render("Speed:", True, TEXT_COLOR)
        SCREEN.blit(lbl_spd, (self.panel_x, 390))

        self.btn_reset.draw(SCREEN)
        self.btn_play.draw(SCREEN)
        self.btn_prev.draw(SCREEN)
        self.btn_next.draw(SCREEN)
        self.btn_end.draw(SCREEN)
        self.dd_speed.draw(SCREEN)

    def loop(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click_board(event.pos)
                self.btn_reset.handle(event)
                self.btn_play.handle(event)
                self.btn_prev.handle(event)
                self.btn_next.handle(event)
                self.btn_end.handle(event)
                self.dd_speed.handle(event)

            self.update()
            SCREEN.fill(WHITE)
            self.draw_grid()
            self.draw_panel()
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    Game().loop()