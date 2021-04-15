import socket
import pygame as pg
import pickle
import json

pg.init()

class Game():
	def __init__(self, address):
		self.sock = socket.socket()

		self.sock.connect(address)
		self.c = self.sock.recv(1024).decode()

		self.size = (800,600)
		self.screen = pg.display.set_mode(self.size)
		pg.display.set_caption("Multiplayer python game, bi-sh")

		self.playerrect = pg.Rect(0, 0, 20, 20)
		self.screenrect = self.screen.get_rect()

		self.colours = {'r':(255,0,0),'g':(0,255,0),'b':(0,0,255)}
		self.velX = 0
		self.velY = 0
		self.speed = 2


	def handleInput(self):
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
			self.handleInput()

			#moving the player and confining within screen
			self.playerrect.move_ip(self.velX, self.velY)
			self.playerrect.clamp_ip(self.screenrect)

			#sending the server player's position
			print((self.playerrect.x, self.playerrect.y, self.c))
			self.sock.send(pickle.dumps((self.playerrect.x, self.playerrect.y, self.c)))

			#get all player positions from server
			playerdata = pickle.loads(self.sock.recv(1024))

			#clear screen, draw player and show screen
			self.screen.fill((0,0,0))
			for i in playerdata:
				if not i[-1] == self.c:
					pg.draw.rect(self.screen, self.colours[i[-1]], pg.Rect(i[0],i[1],20,20))

			pg.draw.rect(self.screen, self.colours[self.c], self.playerrect)

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


