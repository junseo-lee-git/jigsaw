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
                if piece.is_point_inside(x, y):
                    piece.dragging = not piece.dragging

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