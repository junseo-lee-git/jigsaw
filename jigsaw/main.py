# importing pyglet module
import pyglet
import pyglet.window.key
from window import Window

def main():
    # caption i.e title of the window
    title = "Seattle Jigsaw"
    image_path = "images/seattle.png"
    image = pyglet.resource.image(image_path)
    image_width = image.width
    image_height = image.height

    columns = 12
    rows = 11

    window = Window(rows, columns, width = image_width + 325, height = image_height + 300, fullscreen=False)

    output_folder = "pieces_grid"
    window.slice_image_into_grid(image_path, output_folder, rows, columns)

    window.setup_pieces(rows, columns)
        
    # key press event 
    @window.event
    def on_key_press(symbol, modifier):

        # key "C" get press
        if symbol == pyglet.window.key.C:
            print("Key C is pressed")

    # image for icon
    img = image = pyglet.resource.image("images/seattle.png")
    # # setting image as icon
    window.set_icon(img)
                
    # start running the application
    pyglet.app.run()

if __name__ == "__main__":
    main()

