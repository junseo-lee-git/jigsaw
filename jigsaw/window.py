import pyglet
import os
from PIL import Image
from pyglet import shapes
from puzzlePieces import PuzzlePiece

class Window(pyglet.window.Window):
    def __init__(self, rows, columns, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.puzzle_pieces = []
        self.cell_width = 0
        self.cell_height = 0
        self.columns = columns
        self.rows = rows
        self.image = pyglet.resource.image("images/seattle.png")
        # self.piece = PuzzlePiece('images/pikachu.png', 300, 300)
        self.onePiece = -1

    def setup_pieces(self, rows, columns):
        for i in range(rows):
            for j in range(columns):
                image_path = f"pieces_grid/component_{i}_{j}.png"
                self.puzzle_pieces.append(PuzzlePiece(image_path, j * self.cell_width, (rows-1-i) * self.cell_height))

    def on_draw(self):
        self.clear()
        for piece in self.puzzle_pieces:
            piece.draw()
        self.draw_grid()
  
    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            for piece in self.puzzle_pieces:
                if piece.is_point_inside(x, y) and self.onePiece == -1:
                    piece.dragging = not piece.dragging
                    self.onePiece = self.puzzle_pieces.index(piece) # set the onePiece to the index of the curr piece
                elif piece.is_point_inside(x, y) and self.onePiece != self.puzzle_pieces.index(piece):
                    # if clicking another piece, then ignore it
                    pass
                elif piece.is_point_inside(x, y) and self.onePiece == self.puzzle_pieces.index(piece):
                    piece.dragging = not piece.dragging
                    self.onePiece = -1


    def on_mouse_motion(self, x, y, dx, dy):
        for piece in self.puzzle_pieces:
            if piece.dragging:
                piece.sprite.x += dx
                piece.sprite.y += dy
                piece.backdrop.x += dx
                piece.backdrop.y += dy

    def slice_image_into_grid(self, input_image_path, output_folder, rows, columns):
        # Open the input image
        original_image = Image.open(input_image_path)
        
        # Get the dimensions of the original image
        original_width, original_height = original_image.size
        # self.rows = rows
        # self.columns = columns
        
        # Calculate the width and height of each grid cell
        self.cell_width = original_width // columns
        self.cell_height = original_height // rows
        
        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)
        
        # Slice the image into a grid and save each component
        for i in range(rows):
            for j in range(columns):
                left = j * self.cell_width
                upper = i * self.cell_height
                right = (j + 1) * self.cell_width
                lower = (i + 1) * self.cell_height

                # Crop the image to get the component
                component_image = original_image.crop((left, upper, right, lower))
                
                # Save the component image
                component_image.save(f"{output_folder}/component_{i}_{j}.png")

    def draw_grid(self):
        grid_batch = pyglet.graphics.Batch()
        shape_list = []

        # Calculate grid cell size
        cell_width = self.image.width // self.columns
        cell_height = self.image.height // self.rows

        # Draw horizontal lines
        for i in range(0, self.rows + 1):
            y = i * cell_height
            linex = shapes.Line(0, y, self.image.width-4, y, width=3, color=(255, 255, 255), batch=grid_batch)
            shape_list.append(linex)
            
        # Draw vertical lines
        for j in range(0, self.columns + 1):
            x = j * cell_width
            liney = shapes.Line(x, 0, x, self.image.height-10, width=3, color=(255, 255, 255), batch=grid_batch)
            shape_list.append(liney)

        grid_batch.draw()

        image = Image.open('images/puzzlepiece.png')
        rotated0_image = image.resize((cell_width + 20, cell_height + 20))
        rotated0_image.save("rotated0_piece.png")
        rotated90_image = rotated0_image.rotate(90)
        rotated90_image.save("rotated90_piece.png")
        rotated180_image = rotated0_image.rotate(180)
        rotated180_image.save("rotated180_piece.png")
        rotated270_image = rotated0_image.rotate(270)
        rotated270_image.save("rotated270_piece.png")

        rotated0_image = pyglet.image.load("rotated0_piece.png")
        rotated90_image = pyglet.image.load("rotated90_piece.png")
        rotated180_image = pyglet.image.load("rotated180_piece.png")
        rotated270_image = pyglet.image.load("rotated270_piece.png")
        
        i = 0
        for piece in self.puzzle_pieces:
            if i % 2 == 0:
                shape = pyglet.sprite.Sprite(rotated0_image)
            elif i % 2 == 1:
                shape = pyglet.sprite.Sprite(rotated0_image)
            elif i % 2 == 2:
                shape = pyglet.sprite.Sprite(rotated0_image)
            else:
                shape = pyglet.sprite.Sprite(rotated0_image)
            shape.x = piece.sprite.x - 20
            shape.y = piece.sprite.y
            shape.draw()
            i+=1