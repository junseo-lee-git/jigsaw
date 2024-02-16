from pyglet import sprite, resource, shapes
class PuzzlePiece:
    def __init__(self, image_path: str, x: int, y: int):
        self.image = resource.image(image_path)
        # self.sprite = super(PuzzlePiece, self).__init__(self.image)
        self.sprite = sprite.Sprite(self.image)
        self.sprite.x = x
        self.sprite.y = y
        self.dragging = False
        self.backdrop = shapes.BorderedRectangle(x-5, y-5, self.sprite.width + 10, self.sprite.height + 10, border=5, border_color=(255, 0, 0))

    def is_point_inside(self, x, y):
        return (self.sprite.x < x < self.sprite.x + self.sprite.width and
                self.sprite.y < y < self.sprite.y + self.sprite.height)


    def draw(self):
        if self.dragging:
            self.backdrop.draw()
            self.sprite.draw()
        else:
            self.sprite.draw()
