import sys
import pygame
from pygame.sprite import Group
from pygame.sprite import Sprite
import time
import random
global screen
from threading import Timer
#use this to determine if the dino hits a cactus or bird
#multiply time by this to get score
speed = 1
Cacti = Group()
screen = pygame.display.set_mode((1000, 500))
pygame.display.set_caption("Dino Game")

def run_game():
	dead = False
	pygame.init()
	cactus = Cactus(screen)
	Cacti.add(cactus)
	last_milliseconds = pygame.time.get_ticks()
	while not dead:

		#Track elapsed time	
		current_milliseconds = pygame.time.get_ticks()
		elapsed_milliseconds = current_milliseconds - last_milliseconds
		last_milliseconds = current_milliseconds

		dino.update(elapsed_milliseconds)
		update_screen(dino, screen, Cacti)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				check_keydown_events(event, screen, dino, Cacti)
		
			elif event.type == pygame.KEYUP:
				check_keyup_events(event)
		dead = check_collisions(dino, Cacti)
		if determine_cactus():
			cactus = Cactus(screen)
			Cacti.add(cactus)
		
	
	
def update_screen(dino, screen, cacti):
	screen.fill((245, 245, 245))
	pygame.draw.rect(screen,(215,219,108),[0,300,1000,500])
	dino.blitme()
	for cactus in cacti:
		cactus.blitme()
	move_cactus(Cacti)
	pygame.display.flip()
	
class Cactus(Sprite): 
	def __init__(self, screen):
		super(Cactus, self).__init__()
		self.screen = screen
		self.image = pygame.image.load('cactus1.png')
		self.rect = self.image.get_rect()
		
		self.rect.bottom = 300
		self.rect.left = 1000
	def blitme(self):
		self.screen.blit(self.image, self.rect)
		
def determine_score(speed):
	pass
def fall():
	global dino
	dino.rect.bottom += 50
	#print("falling")

def jump(dino, screen, cactus):
	if not dino.is_jumping():
		dino.jump()
	#dino.rect.bottom -= 50
	#t = Timer(1, fall)
	#t.start()

class Dino(Sprite):
	def __init__(self, screen):
		super(Dino, self).__init__()
		self.screen = screen
		self.image = pygame.image.load('thing.png')
		self.rect = self.image.get_rect()
		
		self.rect.bottom = 300
		self.rect.left = 30
		self.bottom = 300

		self.jump_duration_milliseconds = 1000
		self.jump_duration_half_milliseconds = 500
		self.jump_height = 100
		self.jump_curr_duration = 0
		
	def blitme(self):
		self.screen.blit(self.image, self.rect)

	def update(self, delta):
		animation_value = 0
		if self.jump_curr_duration > 0:
			self.jump_curr_duration -= delta
			if self.jump_curr_duration < 0:
				self.jump_curr_duration = 0

		if self.jump_curr_duration > self.jump_duration_half_milliseconds:
			#Rising
			normalized_duration = self.jump_curr_duration - self.jump_duration_half_milliseconds
			duration_percent = 1 - (normalized_duration / self.jump_duration_half_milliseconds)
			animation_value = (int)(self.__cubicEaseOut(duration_percent) * self.jump_height)
		elif self.jump_curr_duration > 0:
			#Falling
			duration_percent = (self.jump_curr_duration / self.jump_duration_half_milliseconds)
			animation_value = (int)(self.__cubicEaseOut(duration_percent) * self.jump_height)

		self.rect.bottom = self.bottom - animation_value
	
	def __cubicEaseOut(self, animation_delta):
		#Use the cubic ease out equation to produce an animation value.
		#delta is expected to be between 0 and 1
		return (1 - pow(1 - animation_delta, 3))

	def jump(self):
		self.jump_curr_duration = self.jump_duration_milliseconds

	def is_jumping(self):
		return self.jump_curr_duration > 0
		
def check_collisions(Dino, cacti):
	for cactus in cacti:
		if pygame.sprite.collide_rect(Dino, cactus):
			return True

def destroy_cactus(Cacti):
	for cactus in Cacti:
		if cactus.rect.right <= 0:
			Cacti.remove(cactus)

def determine_cactus():
	"""a function to determine if a cactus should be placed"""
	x = random.randint(1,1000)
	if x == 50:
		return True
	else:
		return False

def move_cactus(cacti):
	for cactus in cacti:
		cactus.rect.right -= speed
		destroy_cactus(cacti)

	
def check_keydown_events(event, screen, dino, cactus):
	if event.key == pygame.K_UP:
		jump(dino, screen, cactus)
	elif event.key == pygame.K_ESCAPE:
		sys.exit()

def check_keyup_events(event):
	pass

dino = Dino(screen)


	

run_game()
