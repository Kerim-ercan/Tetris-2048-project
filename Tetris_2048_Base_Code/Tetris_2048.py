################################################################################
#                                                                              #
# The main program of Tetris 2048 Base Code                                    #
#                                                                              #
################################################################################

import lib.stddraw as stddraw  # for creating an animation with user interactions
from lib.picture import Picture  # used for displaying an image on the game menu
from lib.color import Color  # used for coloring the game menu
import os  # the os module is used for file and directory operations
from game_grid import GameGrid  # the class for modeling the game grid
from tetromino import Tetromino  # the class for modeling the tetrominoes
from point import Point  # Add this import for Point class
import random  # used for creating tetrominoes with random types (shapes)

# The main function where this program starts execution
def start():
   # set the dimensions of the game grid
   grid_h, grid_w = 20, 12
   # set the size of the drawing canvas (the displayed window)
   canvas_h, canvas_w = 40 * grid_h, 40 * (grid_w + 6)  # Added width for next tetromino
   stddraw.setCanvasSize(canvas_w, canvas_h)
   # set the scale of the coordinate system for the drawing canvas
   stddraw.setXscale(-0.5, grid_w + 5.5)  # Extended scale to show next tetromino
   stddraw.setYscale(-0.5, grid_h - 0.5)

   # set the game grid dimension values stored and used in the Tetromino class
   Tetromino.grid_height = grid_h
   Tetromino.grid_width = grid_w
   # create the game grid
   grid = GameGrid(grid_h, grid_w)
   # create the first tetromino to enter the game grid
   # by using the create_tetromino function defined below
   # create the first tetromino and next tetromino
   current_tetromino = create_tetromino()
   next_tetromino = create_tetromino()  # Add this line
   grid.current_tetromino = current_tetromino

   # display a simple menu before opening the game
   # by using the display_game_menu function defined below
   display_game_menu(grid_h, grid_w)

   # the main game loop
   while True:
      # check for any user interaction via the keyboard
      if stddraw.hasNextKeyTyped():  # check if the user has pressed a key
         key_typed = stddraw.nextKeyTyped()  # the most recently pressed key
         # if the left arrow key has been pressed
         if key_typed == "left":
            # move the active tetromino left by one
            current_tetromino.move(key_typed, grid)
         # if the right arrow key has been pressed
         elif key_typed == "right":
            # move the active tetromino right by one
            current_tetromino.move(key_typed, grid)
         # if the down arrow key has been pressed
         elif key_typed == "down":
            # move the active tetromino down by one
            current_tetromino.move(key_typed, grid)
         elif key_typed == "up":
            current_tetromino.rotate(grid) 
         elif key_typed == "space":
            current_tetromino.hard_drop(grid) 
            
         # clear the queue of the pressed keys for a smoother interaction
         stddraw.clearKeysTyped()

      # move the active tetromino down by one at each iteration (auto fall)
      success = current_tetromino.move("down", grid)
      
      # lock the active tetromino onto the grid when it cannot go down anymore
      if not success:
         # get the tile matrix of the tetromino without empty rows and columns
         # and the position of the bottom left cell in this matrix
         tiles, pos = current_tetromino.get_min_bounded_tile_matrix(True)
         # update the game grid by locking the tiles of the landed tetromino
         game_over = grid.update_grid(tiles, pos)
         # end the main game loop if the game is over
         if game_over:
            stddraw.clear(Color(0, 0, 0))
            stddraw.setFontFamily("Arial")
            stddraw.setFontSize(50)
            stddraw.setPenColor(Color(255, 0, 0))
            stddraw.text((grid_w + 5) / 2, grid_h / 2, "GAME OVER")
            stddraw.setFontSize(30)
            stddraw.setPenColor(Color(255, 255, 255))
            stddraw.text((grid_w + 5) / 2, grid_h / 2 - 1, f"Score: {grid.score}")

            stddraw.show(2000)   # 2 saniye bekle

            # 2) Başlangıç menüsüne dön
            display_game_menu(grid_h, grid_w)

            # 3) Yeni bir oyun başlatmak için grid ve tetrominoları resetle
            grid = GameGrid(grid_h, grid_w)
            current_tetromino = create_tetromino()
            next_tetromino = create_tetromino()
            grid.current_tetromino = current_tetromino

            # Döngünün başına dön ve yeniden oyna
            continue
         # create the next tetromino to enter the game grid
         # by using the create_tetromino function defined below
         current_tetromino = next_tetromino
         next_tetromino = create_tetromino()  # Create new next tetromino
         grid.current_tetromino = current_tetromino

      # display the game grid and next tetromino
      grid.display()
      draw_next_tetromino(next_tetromino)  # Add this line
      stddraw.show(50)  # Add this to update the display

   # print a message on the console when the game is over
   print("Game over")

# A function for creating random shaped tetrominoes to enter the game grid
def create_tetromino():
   # the type (shape) of the tetromino is determined randomly
   tetromino_types = ['I', 'I-90', 'I-270', 'I-180', 'O',
                     'Z', 'Z-90', 'Z-180', 'Z-270', 
                     'T', 'T-90', 'T-180', 'T-270',  # Virgül eklendi
                     'J', 'J-90', 'J-180', 'J-270',
                     'L', 'L-90', 'L-180', 'L-270',
                     'S', 'S-90', 'S-180', 'S-270']
   random_index = random.randint(0, len(tetromino_types) - 1)
   random_type = tetromino_types[random_index]
   # create and return the tetromino
   tetromino = Tetromino(random_type)
   return tetromino

# A function for displaying a simple menu before starting the game
def display_game_menu(grid_height, grid_width):
   # the colors used for the menu
   background_color = Color(42, 69, 99)
   button_color = Color(25, 255, 228)
   text_color = Color(31, 160, 239)
   # clear the background drawing canvas to background_color
   stddraw.clear(background_color)
   # get the directory in which this python code file is placed
   current_dir = os.path.dirname(os.path.realpath(__file__))
   # compute the path of the image file
   img_file = current_dir + "/images/menu_image.png"
   # the coordinates to display the image centered horizontally
   img_center_x = (grid_width + 6) / 2  # tüm canvas'a göre ortala
   img_center_y = grid_height - 7
   
   # the image is modeled by using the Picture class
   image_to_display = Picture(img_file)
   # add the image to the drawing canvas
   stddraw.picture(image_to_display, img_center_x, img_center_y)
   # the dimensions for the start game button
   button_w, button_h = grid_width - 1.5, 2
   # the coordinates of the bottom left corner for the start game button
   button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
   # add the start game button as a filled rectangle
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
   # add the text on the start game button
   stddraw.setFontFamily("Arial")
   stddraw.setFontSize(25)
   stddraw.setPenColor(text_color)
   text_to_display = "Click Here to Start the Game"
   stddraw.text(img_center_x, 5, text_to_display)
   # the user interaction loop for the simple menu
   while True:
      # display the menu and wait for a short time (50 ms)
      stddraw.show(50)
      # check if the mouse has been left-clicked on the start game button
      if stddraw.mousePressed():
         # get the coordinates of the most recent location at which the mouse
         # has been left-clicked
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         # check if these coordinates are inside the button
         if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
               break  # break the loop to end the method and start the game

def draw_next_tetromino(tetromino):
    # Panel position and size
    panel_start_x = Tetromino.grid_width + 0.5  # Moved closer to grid
    panel_start_y = Tetromino.grid_height - 8   # Moved down a bit
    panel_width = 4
    panel_height = 4
    
    # Draw panel background
    stddraw.setPenColor(Color(42, 69, 99))
    stddraw.filledRectangle(panel_start_x, panel_start_y, panel_width, panel_height)
    
    # Draw "Next" text
    stddraw.setPenColor(Color(31, 160, 239))
    stddraw.text(panel_start_x + panel_width/2, panel_start_y + panel_height + 0.5, "Next")
    
    # Center the tetromino in the panel
    n = len(tetromino.tile_matrix)
    start_x = panel_start_x + (panel_width - n) / 2
    start_y = panel_start_y + (panel_height - n) / 2
    
    # Draw tetromino
    for row in range(n):
        for col in range(n):
            if tetromino.tile_matrix[row][col] is not None:
                pos_x = start_x + col
                pos_y = start_y + (n - 1 - row)
                tetromino.tile_matrix[row][col].draw(Point(pos_x, pos_y))



# start() function is specified as the entry point (main function) from which
# the program starts execution
if __name__ == '__main__':
   start()
