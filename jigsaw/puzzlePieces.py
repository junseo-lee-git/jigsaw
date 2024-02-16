from pyglet import sprite, resource, window
class PuzzlePiece:
    def __init__(self, image_path: str, x: int, y: int):
        self.image = resource.image(image_path)
        # self.sprite = super(PuzzlePiece, self).__init__(self.image)
        self.sprite = sprite.Sprite(self.image)
        self.sprite.x = x
        self.sprite.y = y
        self.sprite.scale = 0.5
        self.dragging = False

    def is_point_inside(self, x, y):
        return (self.sprite.x < x < self.sprite.x + self.sprite.width and
                self.sprite.y < y < self.sprite.y + self.sprite.height)



    def draw(self):
        self.sprite.draw()