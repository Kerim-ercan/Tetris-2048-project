import lib.stddraw as stddraw
from lib.color import Color
from point import Point
import numpy as np

class GameGrid:
    def __init__(self, grid_h, grid_w):
        self.grid_height = grid_h
        self.grid_width = grid_w
        self.tile_matrix = np.full((grid_h, grid_w), None)
        self.current_tetromino = None
        self.game_over = False
        self.empty_cell_color = Color(0, 48, 146)
        self.line_color = Color(0, 135, 158)
        self.boundary_color = Color(0, 135, 158)
        self.line_thickness = 0.002
        self.box_thickness = 10 * self.line_thickness
        self.score = 0

    def display(self, clear_screen=True):
        if clear_screen:
            stddraw.clear(self.empty_cell_color)
        self.draw_grid()
        if self.current_tetromino is not None:
            self.current_tetromino.draw()
        self.draw_boundaries()
        stddraw.setPenColor(Color(255, 255, 255))
        stddraw.setFontFamily("Arial")
        stddraw.setFontSize(18)
        stddraw.text(self.grid_width + 2, self.grid_height - 1, f"Score: {self.score}")

    def draw_grid(self):
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                if self.tile_matrix[row][col] is not None:
                    self.tile_matrix[row][col].draw(Point(col, row))
        stddraw.setPenColor(self.line_color)
        stddraw.setPenRadius(self.line_thickness)
        start_x, end_x = -0.5, self.grid_width - 0.5
        start_y, end_y = -0.5, self.grid_height - 0.5
        for x in np.arange(start_x + 1, end_x, 1):
            stddraw.line(x, start_y, x, end_y)
        for y in np.arange(start_y + 1, end_y, 1):
            stddraw.line(start_x, y, end_x, y)
        stddraw.setPenRadius()

    def draw_boundaries(self):
        stddraw.setPenColor(self.boundary_color)
        stddraw.setPenRadius(self.box_thickness)
        stddraw.rectangle(-0.5, -0.5, self.grid_width, self.grid_height)
        stddraw.setPenRadius()

    def is_occupied(self, row, col):
        if not self.is_inside(row, col):
            return False
        return self.tile_matrix[row][col] is not None

    def is_inside(self, row, col):
        return 0 <= row < self.grid_height and 0 <= col < self.grid_width

    def update_grid(self, tiles_to_lock, blc_position):
        self.current_tetromino = None
        # Lock new tiles onto the grid
        n_rows, n_cols = len(tiles_to_lock), len(tiles_to_lock[0])
        for col in range(n_cols):
            for row in range(n_rows):
                if tiles_to_lock[row][col] is not None:
                    pos = Point()
                    pos.x = blc_position.x + col
                    pos.y = blc_position.y + (n_rows - 1) - row
                    if self.is_inside(pos.y, pos.x):
                        self.tile_matrix[pos.y][pos.x] = tiles_to_lock[row][col]
                    else:
                        self.game_over = True
        # Perform merges before clearing rows
        self._merge_tiles()
        # Clear any full rows
        self._clear_full_rows()
        
        return self.game_over

    def _merge_tiles(self):
        # Merge vertically in each column, bottom-to-top, allowing chains
        for col in range(self.grid_width):
            row = 0
            while row < self.grid_height - 1:
                bottom = self.tile_matrix[row][col]
                top = self.tile_matrix[row+1][col]
                if bottom and top and bottom.number == top.number:
                    # Merge into bottom
                    merged_value = bottom.number * 2
                    bottom.number = merged_value
                    bottom.update_colors()
                    self.score += merged_value  # merge puanı   
                    # Shift everything above down
                    for r in range(row+1, self.grid_height-1):
                        self.tile_matrix[r][col] = self.tile_matrix[r+1][col]
                    self.tile_matrix[self.grid_height-1][col] = None
                    # Stay on this row for chain merges
                else:
                    row += 1

    def _clear_full_rows(self):
        row = 0
        while row < self.grid_height:
            if all(self.tile_matrix[row, c] is not None for c in range(self.grid_width)):
                # PUAN EKLEMEK: Satırdaki taşların değerlerini topla
                row_sum = sum(
                    self.tile_matrix[row][c].number for c in range(self.grid_width) if self.tile_matrix[row][c] is not None
                )
                self.score += row_sum  # 👈 toplamı skora ekle

                # Satırı temizle
                self.tile_matrix[row, :] = [None] * self.grid_width
                # Üst satırları aşağı kaydır
                for r in range(row, self.grid_height - 1):
                    self.tile_matrix[r, :] = self.tile_matrix[r + 1, :]
                self.tile_matrix[self.grid_height - 1, :] = [None] * self.grid_width
                # Aynı satırı tekrar kontrol et
            else:
                row += 1