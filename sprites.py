import pygame as pg



class Client(pg.sprite.Sprite):
	def __init__(self, game, color_name, color):

		self.game = game
		self.images = self.game.person_images
		self.groups = self.game.all_sprites, self.game.clients

		pg.sprite.Sprite.__init__(self, self.groups)

		self.color_name = color_name
		self.color = pg.Color(*color)

		self.facing = 0 #[0,3]
		self.moving = False
		self.anim_frame = 1
		self.anim_cycle = 0
		self.frame = 0

		self.rect = pg.Rect(0, 0, self.images[0].get_width(), self.images[0].get_height())
		print(self.images[0].get_width(), self.images[0].get_height())


	def update(self, playerdata, dt):
		for i in playerdata:
			if i[-1] == self.color_name:
				#client is moving
				if self.rect.x - int(i[0]) != 0 or self.rect.y - int(i[1]) != 0: 

					if  self.rect.x - i[0] < 0:  #facing right
						self.facing = 0
					elif self.rect.x - i[0] > 0: #facing left
						self.facing = 3
					self.anim_cycle += dt 
					if self.anim_cycle > 0.15:
						#moving between two frames for now....
						self.anim_frame = 1 if self.anim_frame == 2 else 2
						self.anim_cycle = 0
					self.frame = self.facing + self.anim_frame
				
				else:
					self.frame = self.facing

				self.rect.x = i[0]
				self.rect.y = i[1]
				break
		#if didnt break, means no data for this poor dude
		else:
			print("killin client")
			self.kill()

	def draw(self, surface):
		surface.blit(self.images[self.frame], self.rect)
		pg.draw.polygon(surface, self.color, [(self.rect.x + self.rect.w/2, self.rect.y - 5),
											  (self.rect.x + self.rect.w/4, self.rect.y - self.rect.h/4),
											  (self.rect.x + 3*self.rect.w/4, self.rect.y - self.rect.h/4)])




class Player(pg.sprite.Sprite):
	def __init__(self, game, color_name, color):
		self.game = game
		self.images = self.game.person_images
		self.groups = self.game.all_sprites

		pg.sprite.Sprite.__init__(self, self.groups)

		# img = pg.image.load("res/player.png")
		self.color = pg.Color(*color)
		self.color_name = color_name
	
		self.rect = self.images[0].get_rect()
		self.dir = [0,0]
		self.pos_x = 0
		self.pos_y = 0
		self.speed = 400

		self.facing = 0 #[0,3]
		self.anim_frame = 1
		self.anim_cycle = 0
		self.frame = 0

		#player wont go past this rectangle bounds
		lvl = self.game.level_map
		self.bounds = (lvl.map_width*lvl.rect_size, lvl.map_height*lvl.rect_size)


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

	def animate(self, dt:float):
		if self.dir[0] == 1:
			self.facing = 0
		elif self.dir[0] == -1:
			self.facing = 3

		#character is moving
		if not self.dir == [0,0]:	
			self.anim_cycle += dt
			if self.anim_cycle > 0.15:
				self.frame = self.facing + (1 if self.anim_frame == 2 else 2)
				self.anim_frame = 1 if self.anim_frame == 2 else 2
				self.anim_cycle = 0
		else:
			self.frame = self.facing

	def collision_handle(self, walls:pg.sprite.Group, direction):
		
		if direction == 'x':
			collision_list = pg.sprite.spritecollide(self, walls, False)
			if collision_list:
				if self.dir[0] == -1:
					self.pos_x = collision_list[0].rect.right
				elif self.dir[0] == 1:
					self.pos_x = collision_list[0].rect.x - self.rect.w
				self.dir[0] = 0
				self.rect.x = self.pos_x

		if direction == 'y':
			collision_list = pg.sprite.spritecollide(self, walls, False)
			if collision_list:
				if self.dir[1] == -1:
					self.pos_y = collision_list[0].rect.bottom
				elif self.dir[1] == 1:
					self.pos_y = collision_list[0].rect.y - self.rect.h
				self.dir[1] = 0
				self.rect.y = self.pos_y




	def update(self, dt:float, walls):
		self.pos_x += self.speed*self.dir[0]*dt
		self.pos_y += self.speed*self.dir[1]*dt

		self.animate(dt)	

		if self.pos_x + self.rect.w > self.bounds[0]:
			self.pos_x = self.bounds[0] - self.rect.w
		elif self.pos_x < 0 : 
			self.pos_x = 0
		if self.pos_y + self.rect.h > self.bounds[1]:
			self.pos_y = self.bounds[1] - self.rect.h
		elif self.pos_y < 0:
			self.pos_y = 0

		self.rect.x = self.pos_x
		self.collision_handle(walls, 'x')
		self.rect.y = self.pos_y
		self.collision_handle(walls, 'y')


	def draw(self, surface):
		surface.blit(self.images[self.frame], self.rect)
		pg.draw.polygon(surface, self.color, [(self.rect.x + self.rect.w/2, self.rect.y - 5),
											  (self.rect.x + self.rect.w/4, self.rect.y - self.rect.h/4),
											  (self.rect.x + 3*self.rect.w/4, self.rect.y - self.rect.h/4)])


class Wall(pg.sprite.Sprite):
	def __init__(self, game,  x ,y):
		self.image = pg.image.load("./res/Wall.png")
		self.rect = self.image.get_rect()
		self.game = game

		self.groups = self.game.all_sprites, self.game.walls
		pg.sprite.Sprite.__init__(self, self.groups)

		self.rect.x = x
		self.rect.y = y



