import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from objLoader import ObjLoader
from math import sin, cos, radians

def draw_text(x, y, text, font):
	glPushMatrix()
	glRasterPos2f(x, y)
	for char in text:
		glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(char))
	glPopMatrix()

def main():
	pygame.init()
	display = (800, 600)
	pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

	gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

	radius = 10.0
	yaw = 0.0
	pitch = 0.0
	move_speed = 0.1
	rotate_speed = 2.0

	glEnable(GL_DEPTH_TEST)
	glEnable(GL_TEXTURE_2D)

	try:
		# Nome arquivo .obj
		model = ObjLoader("Car.obj")
	except Exception as e:
		print(f"Erro ao carregar modelo .obj: {e}")
		pygame.quit()
		return

	clock = pygame.time.Clock()
	glutInit()

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				return
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					return

		keys = pygame.key.get_pressed()
		if keys[pygame.K_w]:
			radius = max(1.0, radius - move_speed)
		if keys[pygame.K_s]:
			radius = min(50.0, radius + move_speed)
		if keys[pygame.K_a]:
			yaw += rotate_speed
		if keys[pygame.K_d]:
			yaw -= rotate_speed

		camera_pos = [
			radius * cos(radians(pitch)) * sin(radians(yaw)),
			radius * sin(radians(pitch)),
			radius * cos(radians(pitch)) * cos(radians(yaw))
		]

		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glClearColor(0, 0, 0, 0)

		glLoadIdentity()
		gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
		gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2], 0, 0, 0, 0, 1, 0)

		glPushMatrix()
		glRotatef(15.0, 1, 0, 0)
		glTranslatef(0, -1.0, 0)
		model.draw_with_position(pos=(0, 0, 0), scale=(1, 1, 1))
		glPopMatrix()

		glMatrixMode(GL_PROJECTION)
		glPushMatrix()
		glLoadIdentity()
		gluOrtho2D(0, display[0], 0, display[1])
		glMatrixMode(GL_MODELVIEW)
		glPushMatrix()
		glLoadIdentity()

		glColor3f(1, 1, 1)
		draw_text(10, 90, "W: Move para frente", GLUT_BITMAP_HELVETICA_12)
		draw_text(10, 70, "S: Move para trás", GLUT_BITMAP_HELVETICA_12)
		draw_text(10, 50, "A: Gira à esquerda", GLUT_BITMAP_HELVETICA_12)
		draw_text(10, 30, "D: Gira à direita", GLUT_BITMAP_HELVETICA_12)
		draw_text(10, 10, "ESC: Sair", GLUT_BITMAP_HELVETICA_12)

		glMatrixMode(GL_PROJECTION)
		glPopMatrix()
		glMatrixMode(GL_MODELVIEW)
		glPopMatrix()

		pygame.display.flip()
		clock.tick(60)

if __name__ == "__main__":
	glutInit()
	main()