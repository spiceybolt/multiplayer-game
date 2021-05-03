import pygame as pg

class Map():
	def __init__(self, file_url):
		with open(file_url, 'r') as f:
			self.level = f.read().split('\n')
		self.rect_size = 64
		self.wall_image = pg.image.load("./res/Wall.png")

		self.walls = pg.sprite.Group()

		for row in range(len(self.level)):
			for column in range(len(self.level[row])):
				if self.level[row][column] == '#':
					self.walls.add(Wall(column*self.rect_size, row*self.rect_size, self.wall_image))


	def draw(self, surface):
		self.walls.draw(surface)	

class Wall(pg.sprite.Sprite):
	def __init__(self, x ,y , image):
		pg.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y



