import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from objLoader import ObjLoader
from math import sin, cos, radians

def main():
	pygame.init()
	display = (800, 600)
	pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

	gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

	radius = 10.0
	yaw = 0.0
	pitch = 0.0
	mouse_sensitivity = 0.1
	move_speed = 0.1

	pygame.mouse.set_visible(False)
	pygame.event.set_grab(True)
	glEnable(GL_DEPTH_TEST)
	glEnable(GL_TEXTURE_2D)

	try:
		#  Nome arquivo .obj
		model = ObjLoader("Car.obj")
	except Exception as e:
		print(f"Erro ao carregar modelo .obj: {e}")
		pygame.quit()
		return

	clock = pygame.time.Clock()

	while True:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				return
			if event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					pygame.quit()
					return
			if event.type == MOUSEMOTION:
				if pygame.mouse.get_pressed()[0]:
					dx, dy = event.rel
					yaw -= dx * mouse_sensitivity
					pitch -= dy * mouse_sensitivity
					pitch = max(-89.0, min(89.0, pitch))

		keys = pygame.key.get_pressed()
		if keys[pygame.K_w]:
			radius = max(1.0, radius - move_speed)
		if keys[pygame.K_s]:
			radius = min(50.0, radius + move_speed)

		camera_pos = [
			radius * cos(radians(pitch)) * sin(radians(yaw)),
			radius * sin(radians(pitch)),
			radius * cos(radians(pitch)) * cos(radians(yaw))
		]


		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glClearColor(1, 1, 1, 1)  # Fundo Branco
		# glClearColor(0,0,0,0)  # Fundo Preto

		glLoadIdentity()
		gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
		gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2], 0, 0, 0, 0, 1, 0)

		glPushMatrix()
		model.draw_with_position(pos=(0, 0, 0), scale=(1, 1, 1))
		glPopMatrix()

		pygame.display.flip()
		clock.tick(60)

if __name__ == "__main__":
	glutInit()
	main()