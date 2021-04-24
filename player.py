import socket
import pygame as pg
from time import sleep
import pickle
import json

pg.init()

class Client(pg.sprite.Sprite):
	def __init__(self, color_name, color, image_list):
		pg.sprite.Sprite.__init__(self)

		self.images = image_list

		self.color_name = color_name
		self.color = pg.Color(*color)


		self.rect = pg.Rect(0, 0, self.images[0].get_width(), self.images[0].get_height())


	def update(self, playerdata):
		for i in playerdata:
			if i[-1] == self.color_name:
				self.rect.x = i[0]
				self.rect.y = i[1]
				break
		#if didnt break, means no data for this poor dude
		else:
			self.kill()

	def draw(self, surface):
		surface.blit(self.images[0], self.rect)
		pg.draw.polygon(surface, self.color, [(self.rect.x + self.rect.w/2, self.rect.y),
											  (self.rect.x + self.rect.w/4, self.rect.y - self.rect.h/4),
											  (self.rect.x + 3*self.rect.w/4, self.rect.y - self.rect.h/4)])




class Player(pg.sprite.Sprite):
	def __init__(self, bounds,color_name, color, image_list):
		# super(Player, self).__init__()
		pg.sprite.Sprite.__init__(self)
		self.images = image_list

		# img = pg.image.load("res/player.png")
		self.color = pg.Color(*color)
		self.color_name = color_name
	
		self.rect = self.images[0].get_rect()
		self.dir = [0,0]
		self.pos_x = 0
		self.pos_y = 0
		self.speed = 800

		#player wont go past this rectangle bounds
		self.bounds = bounds


	def set_velocity_x(self,x:int):
		if x > 1 or x < -1 :
			print("only -1,0,1")
			return
		self.dir[0] = x

	def set_velocity_y(self, y:int):
		if y > 1 or y < -1:
			print("only -1,0,1")
			return
		self.dir[1] = y


	def update(self, dt:float):
		self.pos_x += self.speed*self.dir[0]*dt
		self.pos_y += self.speed*self.dir[1]*dt

		if self.pos_x + self.rect.w > self.bounds[0]:
			self.pos_x = self.bounds[0] - self.rect.w
		elif self.pos_x < 0 : 
			self.pos_x = 0
		if self.pos_y + self.rect.h > self.bounds[1]:
			self.pos_y = self.bounds[1] - self.rect.h
		elif self.pos_y < 0:
			self.pos_y = 0


		self.rect.x = self.pos_x
		self.rect.y = self.pos_y


	def draw(self, surface):
		surface.blit(self.images[0], self.rect)
		pg.draw.polygon(surface, self.color, [(self.rect.x + self.rect.w/2, self.rect.y),
											  (self.rect.x + self.rect.w/4, self.rect.y - self.rect.h/4),
											  (self.rect.x + 3*self.rect.w/4, self.rect.y - self.rect.h/4)])



class Game():
	def __init__(self, address):
		#init socket, screen and player and server rects, colours and physics
		self.sock = socket.socket()

		self.sock.connect(address)
		self.c = self.sock.recv(1024).decode()

		self.client_count = 0

		self.size = (800,600)
		self.screen = pg.display.set_mode(self.size)
		pg.display.set_caption("Multiplayer python game, bi-sh")

		self.person_images = []
		self.person_images.append(pg.image.load("res/player.png"))

		self.colours = {'r':(255,0,0),'g':(0,255,0),'b':(0,0,255)}

		self.player = Player(self.size, self.c, self.colours[self.c], self.person_images)
		self.clients = pg.sprite.Group()
		self.clock = pg.time.Clock()


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

	def mainloop(self):	
		while True:
			#getting input from user
			self.handle_input()

			#moving the player and confining within screen
			dt = self.clock.tick()/1000.0

			self.player.update(dt)

			#sending the server player's position
			self.sock.send(pickle.dumps((self.player.pos_x, self.player.pos_y, self.c)))

			#get all player positions from server
			playerdata = pickle.loads(self.sock.recv(1024))

			
			#clear screen, draw player and show screen
			self.screen.fill((255,255,255))

			self.player.draw(self.screen)

			if len(playerdata) > self.client_count + 1 :
				#new dude has joined the connection..
				for each in playerdata:
					if each[-1] != self.player.color_name and each[-1] not in [i.color_name for i in self.clients.sprites()]:
						self.clients.add(Client(each[-1], self.colours[each[-1]], self.person_images))
						print(each[-1])
						self.client_count += 1

					print(each)

			self.clients.update(playerdata)
			for i in self.clients.sprites():
				i.draw(self.screen)

			pg.display.flip()

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


