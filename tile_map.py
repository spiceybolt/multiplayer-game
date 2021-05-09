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

class Camera:
	def __init__(self, level_map, camera_width, camera_height):
		self.height = camera_height
		self.width = camera_width
		#these will be the screen width and height
		self.camera_rect = pg.Rect(0,0,self.width, self.height)
		self.level_width = level_map.map_width*level_map.rect_size - self.width
		self.level_height = level_map.map_height*level_map.rect_size - self.height
		
	def move_rect(self, target):
		return target.rect.move(self.camera_rect.topleft)

	def update(self, target):
		x = -target.rect.x + self.width/2
		y = -target.rect.y + self.height/2

		#limiting camera within level_map
		x = min(0, x)
		y = min(0, y)

		x = max(-self.level_width, x)
		y = max(-self.level_height, y)

		self.camera_rect = pg.Rect(x,y,self.width, self.height)





