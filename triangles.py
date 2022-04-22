import pygame
from random import randrange, randint
from pygame.math import Vector2
from Functions.triangulation import Bowyerwatson, Triangle
from Functions.degradees import gradient

DISPLAY = True
pygame.init()

WIDTH, HEIGHT = 800, 800
BOUNDARYS = WIDTH -1, HEIGHT -1
NB_POINTS = 500
SHOW_VERTICES = False
img_idx = 2

if DISPLAY:
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
else:
	screen = pygame.Surface((WIDTH, HEIGHT))

def random_spreading(NB_POINTS, BOUNDARYS):
	points = []
	while len(points) <NB_POINTS:
		p = [randint(1, BOUNDARYS[0]), randint(1, BOUNDARYS[1])]
		if p not in points:
			points.append(p)

		else:
			print(p)
	
	return points

def filling_outterline(boundaries, pt_per_line):
	"""fonction qui rend des points sur le contour de l'image"""
	pt_per_line = int(pt_per_line)+1

	cell_size = boundaries[0]/pt_per_line, boundaries[1]/pt_per_line

	pts = []
	for i in range(pt_per_line):
		for move_x, move_y in zip([0, WIDTH-1], [0, HEIGHT-1]):
			pts.append([cell_size[0]*i, move_y])
			pts.append([move_x, cell_size[1]*i])
			
	for elem in pts:
		for _ in range(pts.count(elem)-1):
			pts.remove(elem)

	#je trouve pas le probleme et j'ai pas la force
	pts.append([WIDTH-1, HEIGHT-1])
	return pts

### https://angrytools.com/gradient/
points = random_spreading(NB_POINTS, BOUNDARYS)
points += filling_outterline(BOUNDARYS, NB_POINTS/20)
img = pygame.image.load(f"Functions/gradient{img_idx}.png")
Triangle.surface = pygame.transform.scale(img, (WIDTH+1, HEIGHT+1))
Triangle.boundaries = (WIDTH, HEIGHT)

# A = [WIDTH / 2, 2 * HEIGHT]
# B = [2 * WIDTH, -HEIGHT // 8]
# C = [-WIDTH, -HEIGHT // 8 +10]
# SUPER = Triangle([A, B, C], Super = True)

triangulation = Bowyerwatson(points)
for triangle in triangulation:
	triangle.show(screen, draw_vertices = SHOW_VERTICES)

if DISPLAY:
	done = False
	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True

		pygame.display.flip()

pygame.image.save(screen, "Wallpaper.png") 