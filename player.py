import socket
import pygame as pg
import pickle
import json

pg.init()


class Game():
	def __init__(self, address):
		#init socket, screen and player and server rects, colours and physics
		self.sock = socket.socket()

		self.sock.connect(address)
		self.c = self.sock.recv(1024).decode()
		print(self.c)

		self.size = (800,600)
		self.screen = pg.display.set_mode(self.size)
		pg.display.set_caption("Multiplayer python game, bi-sh")

		self.player_rect = pg.Rect(0, 0, 20, 20)
		self.screen_rect = self.screen.get_rect()

		self.colours = {'r':(255,0,0),'g':(0,255,0),'b':(0,0,255)}
		self.velX = 0
		self.velY = 0
		self.speed = 2


	def handle_input(self):
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.quit()
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					self.quit()
				elif event.key == pg.K_UP:
					self.velY = -self.speed
				elif event.key == pg.K_DOWN:
					self.velY = self.speed
				elif event.key == pg.K_LEFT:
					self.velX = -self.speed
				elif event.key == pg.K_RIGHT:
					self.velX = self.speed
			elif event.type == pg.KEYUP:
				if event.key == pg.K_UP or event.key == pg.K_DOWN:
					self.velY = 0
				elif event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
					self.velX = 0


	def mainloop(self):	
			
		while True:
			#getting input from user
			self.handle_input()

			#moving the player and confining within screen
			self.player_rect.move_ip(self.velX, self.velY)
			self.player_rect.clamp_ip(self.screen_rect)

			#sending the server player's position
			self.sock.send(pickle.dumps((self.player_rect.x, self.player_rect.y, self.c)))

			#get all player positions from server
			playerdata = pickle.loads(self.sock.recv(1024))

			#clear screen, draw player and show screen
			self.screen.fill((0,0,0))
			for i in playerdata:
				if not i[-1] == self.c:
					pg.draw.rect(self.screen, self.colours[i[-1]], pg.Rect(i[0],i[1],20,20))

			pg.draw.rect(self.screen, self.colours[self.c], self.player_rect)

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


