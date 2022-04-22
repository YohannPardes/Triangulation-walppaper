from random import randint
import pygame
from itertools import permutations

def ccw (A, B, C):

	for order in list(permutations([A, B, C])):
		a, b, c = order
		if (b[0] - a[0])*(c[1] - a[1])-(c[0] - a[0])*(b[1] - a[1]) > 0:
			return order

		else:
			pass
			# print(f"{(b[0] - a[0])}*{(c[1] - a[1])}-{(c[0] - a[0])}*{(b[1] - a[1])}")

	# print(order)

def inCircle (pts, d):

	a, b, c = ccw(pts[0], pts[1], pts[2])

	ax = a[0]-d[0]
	ay = a[1]-d[1]
	bx = b[0]-d[0]
	by = b[1]-d[1]
	cx = c[0]-d[0]
	cy = c[1]-d[1]

	return (
		(ax *ax  + ay *ay ) * (bx *cy -cx *by ) -
		(bx *bx  + by *by ) * (ax *cy -cx *ay ) +
		(cx *cx  + cy *cy ) * (ax *by -bx *ay )
		) > 0

class Triangle:
	surface = None
	def  __init__(self, pts, Super = False):

		self.sommets = self.A, self.B, self.C = pts if pts else [[randint(0, WIDTH), randint(0, HEIGHT)] for _ in range(3)]

		self.vertices = self.aretes()


	def aretes(self):

		# returning AB, BC, AC, the three vertice of the triangle 
		vertices = [ [self.sommets[i-1], self.sommets[i]] if self.sommets[i-1] > self.sommets[i] else [self.sommets[i], self.sommets[i-1]] for i in range(3)]
		sort_key = lambda x : x[0][0]
		vertices.sort(key = sort_key)

		return vertices

	def show(self, surface, draw_vertices = None):
		self.color = Triangle.surface.get_at([int(n) for n in self.A])
		pygame.draw.polygon(surface, self.color, self.sommets, 0)

		if draw_vertices:
			for v in self.vertices:
				pygame.draw.line(surface, (0,0,0), v[0], v[1], 1)

def find_SuperTriangle(points):
	"""fonction qui trouve le super triangle qui prend tout les points"""

	max_x = points[0][0]
	max_y = points[0][1]
	min_x = points[0][0]
	min_y = points[0][1]

	for p in points:
		if p[0]< min_x:
			min_x = p[0]

		if p[1]< min_y:
			min_y = p[1]

		if p[0] > max_x:
			max_x = p[0]

		if p[1] > max_y:
			max_y = p[1]

	A = [min_x                    , min_y - 1]
	B = [min_x + 2*(max_x - min_x), min_y]
	C = [min_x - 1                , min_y + 2*(max_y - min_y)]

	print(f"A {A}\nB {B}\nC {C}")

	return [A, B, C]

def Bowyerwatson(points):

	SuperTriangle = Triangle(find_SuperTriangle(points))

	triangulation = [SuperTriangle]
	for i, point in enumerate(points):
		if i%100 == 0:
			print(f"{i/len(points):.2%} de la triangulation")
		BadTriangles = []
		potentiallyBadVertices = []
		
		for triangle in triangulation:

			#checking for non delaunys triangles
			# if point_in_circumcircle(triangle.sommets ,point):
			if inCircle(triangle.sommets, point):
				BadTriangles.append(triangle)
				potentiallyBadVertices+=triangle.vertices

		polygon = []
		# deleting non valid vertices
		for triangle in BadTriangles:
			for vertice in triangle.vertices:
				vertice_count = potentiallyBadVertices.count([vertice[0], vertice[1]])
				if vertice_count == 1:
					polygon.append(vertice)

		# creating new triangles
		for vertice in polygon:
			triangulation.append(Triangle([vertice[0], vertice[1], point]))

		triangulation = [triangle for triangle in triangulation if triangle not in BadTriangles]

	# deleting vertices to the supertriangle
	refined_triangulation = []
	for triangle in triangulation:
		for vertice in triangle.vertices:
			if vertice[0] not in SuperTriangle.sommets and vertice[1] not in SuperTriangle.sommets:
				valid = True
				
			else:
				valid = False
				break

		if valid:
			refined_triangulation.append(triangle)

	return refined_triangulation