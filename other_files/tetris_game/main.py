from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple

import pygame


# -----------------------------
# Game constants / tuning
# -----------------------------
GRID_W = 10
GRID_H = 20
HIDDEN_ROWS = 2  # spawn buffer (not rendered)

CELL = 28
PADDING = 18
PANEL_W = 220

FPS = 60
DROP_START_MS = 800
DROP_MIN_MS = 80

LINE_SCORES = {1: 100, 2: 300, 3: 500, 4: 800}


Color = Tuple[int, int, int]


def clamp(v: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, v))


def rotate_cw(cells: Iterable[Tuple[int, int]]) -> List[Tuple[int, int]]:
    # (x, y) -> (y, -x)
    return [(y, -x) for (x, y) in cells]


def rotate_ccw(cells: Iterable[Tuple[int, int]]) -> List[Tuple[int, int]]:
    # (x, y) -> (-y, x)
    return [(-y, x) for (x, y) in cells]


@dataclass(frozen=True)
class PieceDef:
    name: str
    color: Color
    cells: Tuple[Tuple[int, int], ...]  # relative coords around pivot (0,0)


PIECES: List[PieceDef] = [
    PieceDef("I", (0, 240, 240), ((-1, 0), (0, 0), (1, 0), (2, 0))),
    PieceDef("O", (240, 240, 0), ((0, 0), (1, 0), (0, 1), (1, 1))),
    PieceDef("T", (170, 0, 255), ((-1, 0), (0, 0), (1, 0), (0, 1))),
    PieceDef("S", (0, 220, 0), ((0, 0), (1, 0), (-1, 1), (0, 1))),
    PieceDef("Z", (220, 0, 0), ((-1, 0), (0, 0), (0, 1), (1, 1))),
    PieceDef("J", (0, 90, 220), ((-1, 0), (0, 0), (1, 0), (-1, 1))),
    PieceDef("L", (255, 140, 0), ((-1, 0), (0, 0), (1, 0), (1, 1))),
]


class Bag:
    def __init__(self, rng: random.Random):
        self.rng = rng
        self.bag: List[int] = []

    def next_index(self) -> int:
        if not self.bag:
            self.bag = list(range(len(PIECES)))
            self.rng.shuffle(self.bag)
        return self.bag.pop()


@dataclass
class ActivePiece:
    idx: int
    x: int
    y: int
    cells: List[Tuple[int, int]]

    @property
    def defn(self) -> PieceDef:
        return PIECES[self.idx]

    def blocks(self) -> List[Tuple[int, int]]:
        return [(self.x + dx, self.y + dy) for (dx, dy) in self.cells]


class Tetris:
    def __init__(self, rng_seed: Optional[int] = None):
        self.rng = random.Random(rng_seed)
        self.bag = Bag(self.rng)

        self.grid: List[List[Optional[Color]]] = [
            [None for _ in range(GRID_W)] for _ in range(GRID_H + HIDDEN_ROWS)
        ]

        self.score = 0
        self.lines = 0
        self.level = 1
        self.game_over = False
        self.paused = False

        self.active: Optional[ActivePiece] = None
        self.next_idx = self.bag.next_index()

        self.drop_ms = DROP_START_MS
        self.drop_accum = 0.0

        self.lock_delay_ms = 500
        self.lock_timer = 0.0
        self.touched_ground = False

        self.spawn()

    def reset(self) -> None:
        self.__init__()

    def spawn(self) -> None:
        idx = self.next_idx
        self.next_idx = self.bag.next_index()

        cells = [tuple(p) for p in PIECES[idx].cells]

        spawn_x = GRID_W // 2 - 1
        spawn_y = 0

        self.active = ActivePiece(idx=idx, x=spawn_x, y=spawn_y, cells=cells)
        self.touched_ground = False
        self.lock_timer = 0.0

        if self.collides(self.active.blocks()):
            self.game_over = True

    def collides(self, blocks: Iterable[Tuple[int, int]]) -> bool:
        for (x, y) in blocks:
            if x < 0 or x >= GRID_W:
                return True
            if y >= GRID_H + HIDDEN_ROWS:
                return True
            if y >= 0 and self.grid[y][x] is not None:
                return True
        return False

    def try_move(self, dx: int, dy: int) -> bool:
        if not self.active or self.game_over:
            return False
        test = ActivePiece(
            idx=self.active.idx,
            x=self.active.x + dx,
            y=self.active.y + dy,
            cells=self.active.cells[:],
        )
        if self.collides(test.blocks()):
            return False
        self.active = test
        return True

    def try_rotate(self, direction: int) -> bool:
        """
        direction: +1 cw, -1 ccw
        Simple wall-kicks (not full SRS) but feels good in practice.
        """
        if not self.active or self.game_over:
            return False
        if self.active.defn.name == "O":
            return True

        new_cells = (
            rotate_cw(self.active.cells) if direction > 0 else rotate_ccw(self.active.cells)
        )

        kicks = [(0, 0), (-1, 0), (1, 0), (-2, 0), (2, 0), (0, -1)]
        for (kx, ky) in kicks:
            test = ActivePiece(
                idx=self.active.idx,
                x=self.active.x + kx,
                y=self.active.y + ky,
                cells=new_cells,
            )
            if not self.collides(test.blocks()):
                self.active = test
                return True
        return False

    def hard_drop(self) -> None:
        if not self.active or self.game_over:
            return
        dropped = 0
        while self.try_move(0, 1):
            dropped += 1
        self.score += dropped * 2
        self.lock()

    def lock(self) -> None:
        if not self.active or self.game_over:
            return
        color = self.active.defn.color
        for (x, y) in self.active.blocks():
            if y >= 0:
                self.grid[y][x] = color
        self.active = None
        self.clear_lines()
        self.spawn()

    def clear_lines(self) -> None:
        full_rows = [
            y
            for y in range(GRID_H + HIDDEN_ROWS)
            if all(self.grid[y][x] for x in range(GRID_W))
        ]
        if not full_rows:
            return

        for y in full_rows:
            del self.grid[y]
            self.grid.insert(0, [None for _ in range(GRID_W)])

        n = len(full_rows)
        self.lines += n
        self.score += LINE_SCORES.get(n, n * 100) * self.level

        self.level = 1 + self.lines // 10
        self.drop_ms = clamp(DROP_START_MS - (self.level - 1) * 60, DROP_MIN_MS, DROP_START_MS)

    def update(self, dt_ms: float, soft_drop: bool) -> None:
        if self.game_over or self.paused:
            return
        if not self.active:
            return

        speed = 12.0 if soft_drop else 1.0
        self.drop_accum += dt_ms * speed

        while self.drop_accum >= self.drop_ms:
            self.drop_accum -= self.drop_ms
            if not self.try_move(0, 1):
                if not self.touched_ground:
                    self.touched_ground = True
                    self.lock_timer = 0.0
                break
            self.touched_ground = False
            self.lock_timer = 0.0

        if self.touched_ground:
            self.lock_timer += dt_ms
            if self.lock_timer >= self.lock_delay_ms:
                self.lock()

    def ghost_blocks(self) -> List[Tuple[int, int]]:
        if not self.active:
            return []
        test = ActivePiece(
            idx=self.active.idx,
            x=self.active.x,
            y=self.active.y,
            cells=self.active.cells[:],
        )
        while True:
            nxt = ActivePiece(idx=test.idx, x=test.x, y=test.y + 1, cells=test.cells)
            if self.collides(nxt.blocks()):
                return test.blocks()
            test = nxt


def draw_cell(surf: pygame.Surface, color: Color, rect: pygame.Rect) -> None:
    pygame.draw.rect(surf, color, rect, border_radius=4)
    pygame.draw.rect(surf, (15, 15, 20), rect, width=2, border_radius=4)


def main() -> int:
    pygame.init()
    pygame.display.set_caption("Tetris")

    board_w_px = GRID_W * CELL
    board_h_px = GRID_H * CELL

    w = PADDING * 3 + board_w_px + PANEL_W
    h = PADDING * 2 + board_h_px
    screen = pygame.display.set_mode((w, h))

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Segoe UI", 18)
    font_big = pygame.font.SysFont("Segoe UI", 34, bold=True)

    game = Tetris()

    key_repeat = {pygame.K_LEFT: 0.0, pygame.K_RIGHT: 0.0}
    DAS_MS = 140.0
    ARR_MS = 40.0

    def draw_text(lines: List[str], x: int, y: int, big: bool = False, color: Color = (235, 235, 245)) -> None:
        f = font_big if big else font
        yy = y
        for s in lines:
            img = f.render(s, True, color)
            screen.blit(img, (x, yy))
            yy += img.get_height() + 6

    def piece_preview_cells(piece_idx: int) -> List[Tuple[int, int]]:
        cells = list(PIECES[piece_idx].cells)
        minx = min(x for x, _ in cells)
        miny = min(y for _, y in cells)
        return [(x - minx, y - miny) for (x, y) in cells]

    soft_drop = False

    running = True
    while running:
        dt_ms = float(clock.tick(FPS))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break
                if event.key == pygame.K_p:
                    game.paused = not game.paused
                if event.key == pygame.K_r:
                    game = Tetris()
                if game.game_over:
                    continue

                if event.key == pygame.K_UP:
                    game.try_rotate(+1)
                elif event.key == pygame.K_z:
                    game.try_rotate(-1)
                elif event.key == pygame.K_SPACE:
                    game.hard_drop()
                elif event.key == pygame.K_LEFT:
                    game.try_move(-1, 0)
                    key_repeat[pygame.K_LEFT] = 0.0
                elif event.key == pygame.K_RIGHT:
                    game.try_move(1, 0)
                    key_repeat[pygame.K_RIGHT] = 0.0
                elif event.key == pygame.K_DOWN:
                    soft_drop = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    soft_drop = False

        keys = pygame.key.get_pressed()
        for k, dirx in ((pygame.K_LEFT, -1), (pygame.K_RIGHT, 1)):
            if keys[k] and not game.paused and not game.game_over:
                key_repeat[k] += dt_ms
                if key_repeat[k] >= DAS_MS:
                    while key_repeat[k] >= DAS_MS + ARR_MS:
                        if not game.try_move(dirx, 0):
                            break
                        key_repeat[k] -= ARR_MS
            else:
                key_repeat[k] = 0.0

        game.update(dt_ms, soft_drop=soft_drop)

        # -----------------------------
        # Render
        # -----------------------------
        screen.fill((12, 12, 16))

        bx0, by0 = (PADDING, PADDING)
        px0, py0 = (PADDING * 2 + board_w_px, PADDING)

        board_rect = pygame.Rect(bx0, by0, board_w_px, board_h_px)
        pygame.draw.rect(screen, (20, 20, 26), board_rect, border_radius=10)
        pygame.draw.rect(screen, (40, 40, 55), board_rect, width=2, border_radius=10)

        # stacked cells
        for y in range(GRID_H):
            gy = y + HIDDEN_ROWS
            for x in range(GRID_W):
                c = game.grid[gy][x]
                if c is None:
                    continue
                rx = bx0 + x * CELL
                ry = by0 + y * CELL
                rect = pygame.Rect(rx + 1, ry + 1, CELL - 2, CELL - 2)
                draw_cell(screen, c, rect)

        # ghost
        ghost = game.ghost_blocks()
        if ghost and game.active and not game.game_over:
            ghost_color = tuple(int(v * 0.35) for v in game.active.defn.color)
            for (x, y) in ghost:
                if y < HIDDEN_ROWS:
                    continue
                rx = bx0 + x * CELL
                ry = by0 + (y - HIDDEN_ROWS) * CELL
                rect = pygame.Rect(rx + 4, ry + 4, CELL - 8, CELL - 8)
                pygame.draw.rect(screen, ghost_color, rect, width=2, border_radius=4)

        # active piece
        if game.active:
            for (x, y) in game.active.blocks():
                if y < HIDDEN_ROWS:
                    continue
                rx = bx0 + x * CELL
                ry = by0 + (y - HIDDEN_ROWS) * CELL
                rect = pygame.Rect(rx + 1, ry + 1, CELL - 2, CELL - 2)
                draw_cell(screen, game.active.defn.color, rect)

        # panel
        panel_rect = pygame.Rect(px0, py0, PANEL_W, board_h_px)
        pygame.draw.rect(screen, (16, 16, 22), panel_rect, border_radius=10)
        pygame.draw.rect(screen, (40, 40, 55), panel_rect, width=2, border_radius=10)

        draw_text(["分数", f"{game.score}"], px0 + 16, py0 + 18)
        draw_text(["等级", f"{game.level}"], px0 + 16, py0 + 84)
        draw_text(["消行", f"{game.lines}"], px0 + 16, py0 + 150)

        draw_text(["下一个"], px0 + 16, py0 + 220, big=False)
        preview = piece_preview_cells(game.next_idx)
        pr_cell = 22
        offx = px0 + 26
        offy = py0 + 260
        col = PIECES[game.next_idx].color
        for (x, y) in preview:
            rect = pygame.Rect(offx + x * pr_cell, offy + y * pr_cell, pr_cell - 2, pr_cell - 2)
            pygame.draw.rect(screen, col, rect, border_radius=4)
            pygame.draw.rect(screen, (15, 15, 20), rect, width=2, border_radius=4)

        help_lines = [
            "← → 移动",
            "↑ 旋转 / Z 反旋",
            "↓ 软降 / Space 硬降",
            "P 暂停  R 重开",
            "Esc 退出",
        ]
        draw_text(["操作"] + help_lines, px0 + 16, py0 + 360, big=False, color=(200, 200, 215))

        if game.paused and not game.game_over:
            overlay = pygame.Surface((board_w_px, board_h_px), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 130))
            screen.blit(overlay, (bx0, by0))
            draw_text(["暂停"], bx0 + 70, by0 + 150, big=True)

        if game.game_over:
            overlay = pygame.Surface((board_w_px, board_h_px), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 170))
            screen.blit(overlay, (bx0, by0))
            draw_text(["GAME OVER"], bx0 + 26, by0 + 120, big=True, color=(255, 220, 220))
            draw_text(["按 R 重新开始"], bx0 + 54, by0 + 180, big=False)

        pygame.display.flip()

    pygame.quit()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

