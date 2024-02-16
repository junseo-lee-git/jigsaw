import pyglet
from puzzlePieces import PuzzlePiece

class Window(pyglet.window.Window):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.piece = PuzzlePiece('images/pikachu.png', 300, 300)

    def on_draw(self):
        self.clear()
        self.piece.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            if self.piece.is_point_inside(x, y):
                self.piece.dragging = not self.piece.dragging

    def on_mouse_motion(self, x, y, dx, dy):
        if self.piece.dragging:
            self.piece.sprite.x += dx
            self.piece.sprite.y += dy
            self.piece.backdrop.x += dx
            self.piece.backdrop.y += dy