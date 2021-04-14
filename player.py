import socket
import pygame as pg
import pickle
import json

class Game():
	def __init__(self, address):
		self.sock = socket.socket()

		self.sock.connect(address)
		self.c = self.sock.recv(1024).decode()



	def mainloop(self):	
		x,y,xp,yp = 0,0,0,0
		sent = None
		while True:
			xp = int(input("x: "))
			yp = int(input("y: "))
			if xp == -1 or yp == -1:
				break
			x += xp
			y += yp
			sent = pickle.dumps((x,y,self.c))
			print(len(sent),": len of pickle object")
			self.sock.send(sent)
			print(self.sock.recv(1024))
		self.sock.send(b'')
		self.quit()

	def quit(self):
		self.sock.close()

with open('config.json','r') as f:
	data = json.load(f)

port = data["port"]
game = Game((socket.gethostname(), port))
game.mainloop()


