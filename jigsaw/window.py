import pyglet
import os
from PIL import Image
from draggableRectangle import DraggableRectangle
from pyglet.sprite import Sprite

class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.rectangle = DraggableRectangle(500, 500, 50, 50)
        self.cell_width = 0
        self.cell_height = 0

    def on_draw(self):
        self.clear()
        self.rectangle.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            if self.rectangle.is_point_inside(x, y):
                self.rectangle.is_dragging = not self.rectangle.is_dragging
                print(self.rectangle.is_dragging)

    def on_mouse_release(self, x, y, button, modifiers):
        # if button == pyglet.window.mouse.LEFT:
        #     self.rectangle.is_dragging = False
        pass

    def on_mouse_motion(self, x, y, dx, dy):
        if self.rectangle.is_dragging is True:
            # self.rectangle.x += dx
            # self.rectangle.y += dy
            self.rectangle.x = x - self.rectangle.width / 2
            self.rectangle.y = y - self.rectangle.height / 2

    def slice_image_into_grid(self, input_image_path, output_folder, rows, columns):
        # Open the input image
        original_image = Image.open(input_image_path)
        
        # Get the dimensions of the original image
        original_width, original_height = original_image.size
        
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

    # Function to load an image file and create a sprite
    def load_sprite(self, image_path, x, y):
        image = pyglet.image.load(image_path)
        sprite = Sprite(image, x=x, y=y)
        return sprite

    # Function to load all generated images into sprites
    def load_all_sprites(self, folder_path, rows, columns):
        sprites = []
        
        for i in range(rows):
            for j in range(columns):
                image_path = f"{folder_path}/component_{i}_{j}.png"
                sprite = self.load_sprite(image_path, j * self.cell_width, i * self.cell_height)
                sprites.append(sprite)
        
        return sprites