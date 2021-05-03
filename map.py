import pygame as pg

class Map():
	def __init__(self, file_url):
		with open(file_url, 'r') as f:
			self.level = f.read().split('\n')
		self.rect_size = 64


	def draw(self, surface):
		for row in range(len(self.level)):
			for column in range(len(self.level[row])):
				if self.level[row][column] == '#':
					pg.draw.rect(surface,(0,255,0),(row*self.rect_size, column*self.rect_size))					


