import lib.stddraw as stddraw
from lib.color import Color
import random  # used for setting initial tile values

class Tile:
    # Class variables
    boundary_thickness = 0.004
    font_family, font_size = "Arial", 14

    # Map tile values to background colors
    VALUE_TO_COLOR = {
        2: Color(238, 228, 218),
        4: Color(237, 224, 200),
        8: Color(242, 177, 121),
        16: Color(245, 149, 99),
        32: Color(246, 124, 95),
        64: Color(246, 94, 59),
        128: Color(237, 207, 114),
        256: Color(237, 204, 97),
        512: Color(237, 200, 80),
        1024: Color(237, 197, 63),
        2048: Color(237, 194, 46),
    }
    # Map tile values to text colors for contrast
    VALUE_TO_TEXT_COLOR = {
        2: Color(119, 110, 101),
        4: Color(119, 110, 101),
    }
    DEFAULT_TEXT_COLOR = Color(249, 246, 242)
    DEFAULT_BG_COLOR = Color(205, 193, 180)

    def __init__(self):
        # Initialize with 2 or 4
        self.number = random.choice([2, 4])
        # Assign colors based on value
        self.update_colors()
        # Fixed border color
        self.box_color = Color(0, 100, 200)

    def update_colors(self):
        # Background reflects tile value
        self.background_color = Tile.VALUE_TO_COLOR.get(self.number, Tile.DEFAULT_BG_COLOR)
        # Text color for readability
        self.foreground_color = Tile.VALUE_TO_TEXT_COLOR.get(self.number, Tile.DEFAULT_TEXT_COLOR)

    def draw(self, position, length=1):
        # Draw tile background
        stddraw.setPenColor(self.background_color)
        stddraw.filledSquare(position.x, position.y, length / 2)
        # Draw border
        stddraw.setPenColor(self.box_color)
        stddraw.setPenRadius(Tile.boundary_thickness)
        stddraw.square(position.x, position.y, length / 2)
        stddraw.setPenRadius()
        # Draw number
        stddraw.setPenColor(self.foreground_color)
        stddraw.setFontFamily(Tile.font_family)
        stddraw.setFontSize(Tile.font_size)
        stddraw.text(position.x, position.y, str(self.number))
