import json
import os
import random
import pyxel

# --- HALVED RESOLUTION FOR BIGGER NATIVE TEXT ---
SCREEN_WIDTH = 260
SCREEN_HEIGHT = 360
FPS = 60    

COLS = 10
ROWS = 20
BLOCK = 15  # Halved block size
BOARD_X = 20
BOARD_Y = 30
BOARD_W = COLS * BLOCK
BOARD_H = ROWS * BLOCK
SIDE_X = BOARD_X + BOARD_W + 16
PANEL_W = 65

DROP_BASE = 30
LOCK_DELAY = 20
SCORE_FILE = os.path.join(os.path.dirname(__file__), "pyxel_tetris_highscore.json")

SHAPES = {
    "I": [[1, 1, 1, 1]],
    "O": [[1, 1], [1, 1]],
    "T": [[0, 1, 0], [1, 1, 1]],
    "S": [[0, 1, 1], [1, 1, 0]],
    "Z": [[1, 1, 0], [0, 1, 1]],
    "J": [[1, 0, 0], [1, 1, 1]],
    "L": [[0, 0, 1], [1, 1, 1]],
}

COLORS = {
    "I": 12, "O": 10, "T": 2, "S": 11, "Z": 8, "J": 1, "L": 9,
}

# Tetris-style line scores from Code 1
LINE_SCORES = {1: 100, 2: 300, 3: 500, 4: 800}


class Piece:
    def __init__(self, kind=None):
        self.kind = kind or random.choice(list(SHAPES.keys()))
        self.shape = [row[:] for row in SHAPES[self.kind]]
        self.color = COLORS[self.kind]
        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotated(self):
        return [list(row) for row in zip(*self.shape[::-1])]


class TetrisApp:
    def __init__(self):
        # display_scale=2 makes the window 520x720 on your monitor,
        # but internal pixels (and text) are 2x bigger!
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Tetris", fps=FPS, display_scale=2)
        self.high_score = self.load_high_score()
        self.reset_game()
        pyxel.run(self.update, self.draw)

    def load_high_score(self):
        try:
            with open(SCORE_FILE, "r", encoding="utf-8") as f:
                return int(json.load(f).get("high_score", 0))
        except Exception:
            return 0

    def save_high_score(self):
        try:
            with open(SCORE_FILE, "w", encoding="utf-8") as f:
                json.dump({"high_score": self.high_score}, f)
        except Exception:
            pass

    def reset_game(self):
        self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.score = 0
        self.lines = 0
        # Match Code 1 semantics: level starts at 1
        self.level = 1
        self.drop_timer = 0
        self.lock_timer = 0
        self.paused = False
        self.game_over = False
        self.current = Piece()
        self.next_piece = Piece()
        if self.collision(self.current, self.current.x, self.current.y):
            self.game_over = True

    def update_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()

    def collision(self, piece, nx, ny, shape=None):
        shape = shape or piece.shape
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if not cell:
                    continue
                bx = nx + x
                by = ny + y
                if bx < 0 or bx >= COLS or by >= ROWS:
                    return True
                if by >= 0 and self.board[by][bx]:
                    return True
        return False

    def merge_piece(self):
        for y, row in enumerate(self.current.shape):
            for x, cell in enumerate(row):
                if cell:
                    by = self.current.y + y
                    bx = self.current.x + x
                    if 0 <= by < ROWS and 0 <= bx < COLS:
                        self.board[by][bx] = self.current.color
        self.clear_lines()
        self.spawn_piece()

    def spawn_piece(self):
        self.current = self.next_piece
        self.current.x = COLS // 2 - len(self.current.shape[0]) // 2
        self.current.y = 0
        self.next_piece = Piece()
        self.lock_timer = 0
        if self.collision(self.current, self.current.x, self.current.y):
            self.game_over = True
            self.update_high_score()

    def clear_lines(self):
        cleared = 0
        new_board = []
        for row in self.board:
            if all(row):
                cleared += 1
            else:
                new_board.append(row)
        while len(new_board) < ROWS:
            new_board.insert(0, [0] * COLS)
        self.board = new_board

        if cleared:
            self.lines += cleared

            # Match Code 1 level logic: +1 level every 10 lines, starting from 1
            self.level = self.lines // 10 + 1

            base = LINE_SCORES.get(cleared, 0)
            # Match Code 1 formula: score += base * level
            self.score += base * self.level

            self.update_high_score()

    def move(self, dx):
        if not self.collision(self.current, self.current.x + dx, self.current.y):
            self.current.x += dx
            self.lock_timer = 0

    def rotate(self):
        rotated = self.current.rotated()
        kicks = [0, -1, 1, -2, 2]
        for dx in kicks:
            if not self.collision(self.current, self.current.x + dx, self.current.y, rotated):
                self.current.shape = rotated
                self.current.x += dx
                self.lock_timer = 0
                return

    def soft_drop(self):
        # 1 point per soft-dropped row (same as Code 1)
        if not self.collision(self.current, self.current.x, self.current.y + 1):
            self.current.y += 1
            self.score += 1
            self.update_high_score()
            return True
        return False

    def hard_drop(self):
        # 2 points per hard-dropped row (same as Code 1)
        steps = 0
        while not self.collision(self.current, self.current.x, self.current.y + 1):
            self.current.y += 1
            steps += 1
        self.score += steps * 2
        self.update_high_score()
        self.merge_piece()

    def ghost_y(self):
        gy = self.current.y
        while not self.collision(self.current, self.current.x, gy + 1):
            gy += 1
        return gy

    def handle_input(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_R):
            self.reset_game()
            return
        if pyxel.btnp(pyxel.KEY_P) and not self.game_over:
            self.paused = not self.paused

        if self.paused or self.game_over:
            return

        if pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.KEY_A):
            self.move(-1)
        if pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.KEY_D):
            self.move(1)
        if pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.KEY_W):
            self.rotate()
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.hard_drop()
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
            if pyxel.frame_count % 3 == 0 and not self.game_over:
                self.soft_drop()

    def auto_drop_speed(self):
        # You can keep this independent of Code 1 if you like
        return max(5, DROP_BASE - (self.level * 2))

    def update(self):
        self.handle_input()
        if self.paused or self.game_over:
            return

        self.drop_timer += 1
        if self.drop_timer >= self.auto_drop_speed():
            self.drop_timer = 0
            if not self.collision(self.current, self.current.x, self.current.y + 1):
                self.current.y += 1
            else:
                self.lock_timer += 1
                if self.lock_timer >= LOCK_DELAY:
                    self.merge_piece()
                    self.lock_timer = 0
        elif self.collision(self.current, self.current.x, self.current.y + 1):
            self.lock_timer += 1
            if self.lock_timer >= LOCK_DELAY:
                self.merge_piece()
                self.lock_timer = 0
        else:
            self.lock_timer = 0

    def draw_block(self, x, y, color, ghost=False):
        px = BOARD_X + x * BLOCK
        py = BOARD_Y + y * BLOCK

        if ghost:
            pyxel.rectb(px + 1, py + 1, BLOCK - 2, BLOCK - 2, 13)
            return

        pyxel.rect(px + 1, py + 1, BLOCK - 2, BLOCK - 2, color)
        pyxel.line(px + 1, py + 1, px + BLOCK - 2, py + 1, 7)
        pyxel.line(px + 1, py + 1, px + 1, py + BLOCK - 2, 7)
        pyxel.line(px + BLOCK - 2, py + 1, px + BLOCK - 2, py + BLOCK - 2, 5)
        pyxel.line(px + 1, py + BLOCK - 2, px + BLOCK - 2, py + BLOCK - 2, 5)

    def draw_piece_preview(self, piece, px, py):
        size = 16  # Scaled down for the new resolution
        shape = piece.shape
        shape_w = len(shape[0]) * size
        shape_h = len(shape) * size

        box_w = PANEL_W - 6
        box_h = 63 - 12
        offset_x = px + (box_w - shape_w) // 2
        offset_y = py + (box_h - shape_h) // 2

        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    bx = offset_x + x * size
                    by = offset_y + y * size
                    pyxel.rect(bx + 1, by + 1, size - 2, size - 2, piece.color)
                    pyxel.rectb(bx, by, size, size, 7)

    def draw(self):
        pyxel.cls(0)

        # Board border
        pyxel.rectb(BOARD_X - 1, BOARD_Y - 1, BOARD_W + 2, BOARD_H + 2, 7)

        # Board grid + locked blocks
        for y in range(ROWS):
            for x in range(COLS):
                px = BOARD_X + x * BLOCK
                py = BOARD_Y + y * BLOCK
                pyxel.rectb(px, py, BLOCK, BLOCK, 5)
                color = self.board[y][x]
                if color:
                    self.draw_block(x, y, color)

        # Ghost piece
        gy = self.ghost_y()
        for y, row in enumerate(self.current.shape):
            for x, cell in enumerate(row):
                if cell:
                    by = gy + y
                    bx = self.current.x + x
                    if by >= 0:
                        self.draw_block(bx, by, self.current.color, ghost=True)

        # Current piece
        for y, row in enumerate(self.current.shape):
            for x, cell in enumerate(row):
                if cell:
                    by = self.current.y + y
                    bx = self.current.x + x
                    if by >= 0:
                        self.draw_block(bx, by, self.current.color)

        # --- Right side panel ---
        pyxel.text(SIDE_X, 12, "Tetris", 10)

        pyxel.text(SIDE_X, 43, "Next", 7)
        pyxel.rectb(SIDE_X, 59, PANEL_W, 63, 7)
        self.draw_piece_preview(self.next_piece, SIDE_X + 3, 59 + 3)

        stats_y = 135
        pyxel.text(SIDE_X, stats_y,       f"Score: {self.score}", 7)
        pyxel.text(SIDE_X, stats_y + 15,  f"Lines: {self.lines}", 7)
        pyxel.text(SIDE_X, stats_y + 30,  f"Level: {self.level}", 7)
        pyxel.text(SIDE_X, stats_y + 45,  f"Best: {self.high_score}", 10)

        ctrl_y = 215
        pyxel.text(SIDE_X, ctrl_y, "Controls", 7)

        controls = [
            "L/R or A/D: Move",
            "Up or W: Rotate",
            "Down/S: Soft drop",
            "Space: Hard drop",
            "P: Pause",
            "R: Restart",
            "Esc: Quit",
        ]
        for i, line in enumerate(controls):
            pyxel.text(SIDE_X, ctrl_y + 15 + i * 12, line, 13)

        # Pause overlay
        if self.paused and not self.game_over:
            box_w, box_h = 130, 40
            box_x = BOARD_X + (BOARD_W - box_w) // 2
            box_y = BOARD_Y + (BOARD_H - box_h) // 2
            pyxel.rect(box_x, box_y, box_w, box_h, 0)
            pyxel.rectb(box_x, box_y, box_w, box_h, 7)
            pyxel.text(box_x + 45, box_y + 10, "PAUSED", 10)
            pyxel.text(box_x + 15, box_y + 25, "Press P to continue", 7)

        # Game over overlay
        if self.game_over:
            msg_y = BOARD_Y + BOARD_H // 2 - 8
            pyxel.rect(BOARD_X + 15, msg_y - 5, 120, 30, 0)
            pyxel.rectb(BOARD_X + 15, msg_y - 5, 120, 30, 8)
            pyxel.text(BOARD_X + 40, msg_y, "GAME OVER", 8)
            pyxel.text(BOARD_X + 22, msg_y + 15, "Press R to restart", 7)


if __name__ == "__main__":
    TetrisApp()