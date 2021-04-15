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
			self.handleInput()

			self.playerrect.move_ip(self.velX, self.velY)
			self.playerrect.clamp_ip(self.screenrect)

			print((self.playerrect.x, self.playerrect.y, self.c))
			self.sock.send(pickle.dumps((self.playerrect.x, self.playerrect.y, self.c)))

			self.screen.fill((0,0,0))
			pg.draw.rect(self.screen, self.colours[self.c], self.playerrect)

			pg.display.flip()
		# x,y,xp,yp = 0,0,0,0
		# sent = None
		# while True:
		# 	xp = int(input("x: "))
		# 	yp = int(input("y: "))
		# 	if xp == -1 or yp == -1:
		# 		break
		# 	x += xp
		# 	y += yp
		# 	sent = pickle.dumps((x,y,self.c))
		# 	print(len(sent),": len of pickle object")
		# 	self.sock.send(sent)
		# 	print(self.sock.recv(1024))
		# self.sock.send(b'')
		# self.quit()

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


