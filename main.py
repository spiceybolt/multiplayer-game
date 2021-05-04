import socket
import pygame as pg
from time import sleep
import pickle
import json

import sprites
import tile_map

pg.init()


class Game():
	def __init__(self, address):
		#init socket
		self.sock = socket.socket()

		self.sock.connect(address)
		self.c = self.sock.recv(1024).decode()

		#number of clients, size and pygame stuff
		self.client_count = 0

		self.size = (800,600)
		self.screen = pg.display.set_mode(self.size)
		pg.display.set_caption("Multiplayer python game, bi-sh")

		#player images
		self.person_images = []
		for i in range(6):
			self.person_images.append(pg.image.load(f"./res/player/sprite{i}.png"))

		#all colours we might use
		self.colours = {'r':(255,0,0),'g':(0,255,0),'b':(0,0,255)}

		#player, clients , maps and groups
		self.all_sprites = pg.sprite.Group()
		self.clients = pg.sprite.Group()
		self.walls = pg.sprite.Group()

		self.player = sprites.Player(self, self.c, self.colours[self.c])
		self.level_map = tile_map.Map("res/levels/level1.txt")
		self.init_map()
		self.clock = pg.time.Clock()

	def init_map(self):
		for row in range(self.level_map.map_height):
			for column in range(self.level_map.map_width):
				if self.level_map.level_data[row][column] == '#':
					sprites.Wall(self, column*self.level_map.rect_size, row*self.level_map.rect_size)

	def handle_input(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.quit()

			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					self.quit()
				elif event.key == pg.K_UP:
					self.player.set_velocity_y(-1)
				elif event.key == pg.K_DOWN:
					self.player.set_velocity_y(1)
				elif event.key == pg.K_LEFT:
					self.player.set_velocity_x(-1)
				elif event.key == pg.K_RIGHT:
					self.player.set_velocity_x(1)
			
			elif event.type == pg.KEYUP:
				if event.key == pg.K_UP or event.key == pg.K_DOWN:
					self.player.set_velocity_y(0)
				elif event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
					self.player.set_velocity_x(0)

	def handle_client(self, playerdata):
			if len(playerdata) < self.client_count + 1:
				# a dude has exited the connection....
				self.client_count -= 1

			if len(playerdata) > self.client_count + 1 :
				#new dude has joined the connection..
				for each in playerdata:
					if each[-1] != self.player.color_name and each[-1] not in [i.color_name for i in self.clients.sprites()]:
						sprites.Client(self,each[-1], self.colours[each[-1]])
						for i in self.clients.sprites():
							print(i.color_name)
						self.client_count += 1		

	def draw(self):
		#clearing the screen and drawing all entities
		self.screen.fill((112,128,144))

		self.walls.draw(self.screen)

		self.player.draw(self.screen)

		for i in self.clients.sprites():
			i.draw(self.screen)

		pg.display.flip()
	
	def mainloop(self):	
		while True:
			#getting input from user
			self.handle_input()

			dt = self.clock.tick()/1000.0

			#updating player data and sending to server
			self.player.update(dt, self.walls)
			self.sock.send(pickle.dumps((self.player.pos_x, self.player.pos_y, self.c)))

			#get all player positions from server
			playerdata = pickle.loads(self.sock.recv(1024))

			#handle client connections and update client sprites
			self.handle_client(playerdata)
			self.clients.update(playerdata, dt)

			self.draw()

	def quit(self):
		print("Exiting")
		pg.quit()

		self.sock.send(b'')
		self.sock.close()

		exit()



with open('config.json','r') as f:
	data = json.load(f)

port = data["port"]
game = Game((socket.gethostname(), port))
game.mainloop()