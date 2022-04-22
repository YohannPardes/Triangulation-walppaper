import pygame
from pygame.math import Vector2

class Pixel:

	liste_pixel = []
	def __init__(self, WIDTH, HEIGHT, clmns):
		self.size_x, self.size_y = WIDTH//clmns, HEIGHT//clmns 

		self.index = len(Pixel.liste_pixel)
		self.pos = Vector2((self.index%clmns)*self.size_x, (self.index//clmns)*self.size_y)
		self.color = (mapNbs(self.pos.y, 0, WIDTH, 0, 255), mapNbs(self.pos.y, 0, WIDTH, 150, 255), 0)


		Pixel.liste_pixel.append(self)

	def show(self, surface):

		pygame.draw.rect(surface, self.color, ((int(self.pos.x),int(self.pos.y)), (self.size_x, self.size_y)))

def mapNbs (nb ,x1, y1, x2, y2):

	#adding the offset
	nb += x2-x1

	#stretching to the ratio
	nb*=(y2-x2)/(y1-x2)

	return nb

def gradient(WIDTH, HEIGHT, resolution = None):

	if resolution:
		clmns = resolution

	else:
		clmns = int(WIDTH*0.5)

	rows = clmns

	drawing_surface = pygame.display.set_mode((WIDTH, HEIGHT))
	for _ in range((clmns)*(rows)):
		p = Pixel(WIDTH, HEIGHT, clmns)
		p.show(drawing_surface)

	pygame.image.save(drawing_surface, "gradient.png")

	return drawing_surface