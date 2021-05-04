import pygame as pg

class Map():
	def __init__(self, file_url):
		self.level_data = []
		with open(file_url, 'r') as f:
			for line in f:
				self.level_data.append(line.strip())
		self.rect_size = 64
		self.map_width = len(self.level_data[0])
		self.map_height = len(self.level_data)






