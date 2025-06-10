import pygame
from OpenGL.GL import *
import os

class ObjLoader:
	def __init__(self, filename):
		self.vertices = []
		self.normals = []
		self.texcoords = []
		self.faces = []
		self.materials = {}
		self.current_material = None
		self.textures = {}
		self.load_obj(filename)
		self.override_colors = {}

	def load_mtl(self, mtl_file, base_path):
		if not os.path.exists(mtl_file):
			print(f"Erro ao carregar arquivo '.mtl': {mtl_file}")
			return
		try:
			with open(mtl_file, 'r') as file:
				current_mat = None
				for line in file:
					if line.startswith('#'):
						continue
					values = line.strip().split()
					if not values:
						continue
					if values[0] == 'newmtl':
						current_mat = values[1]
						self.materials[current_mat] = {'map_Kd': None, 'Kd': [1, 1, 1]}
					elif values[0] == 'map_Kd' and current_mat:
						texture_path = os.path.join(base_path, values[1])
						self.materials[current_mat]['map_Kd'] = texture_path
						if not os.path.exists(texture_path):
							print(f"Erro textura '{texture_path}' não encontrada.")
							continue
						try:
							surface = pygame.image.load(texture_path)
							image = pygame.image.tostring(surface, "RGBA", 1)
							width, height = surface.get_size()
							texture_id = glGenTextures(1)
							glBindTexture(GL_TEXTURE_2D, texture_id)
							glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
							glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
							glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
							glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
							glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
							self.textures[current_mat] = texture_id
						except Exception as e:
							print(f"Erro ao carregar a textura: {texture_path}: {e}")
					elif values[0] == 'Kd' and current_mat:
						self.materials[current_mat]['Kd'] = list(map(float, values[1:4]))
		except Exception as e:
			print(f"Erro ao carregar arquivo '.mtl': {e}")

	def load_obj(self, filename):
		base_path = os.path.dirname(filename)
		if not os.path.exists(filename):
			return
		try:
			with open(filename, 'r') as file:
				for line in file:
					if line.startswith('#'):
						continue
					values = line.strip().split()
					if not values:
						continue
					if values[0] == 'v':
						self.vertices.append(list(map(float, values[1:4])))
					elif values[0] == 'vn':
						self.normals.append(list(map(float, values[1:4])))
					elif values[0] == 'vt':
						self.texcoords.append(list(map(float, values[1:3])))
					elif values[0] == 'f':
						face = []
						for v in values[1:]:
							indices = v.split('/')
							face.append([int(i) if i else 0 for i in indices])
						self.faces.append((face, self.current_material))
					elif values[0] == 'usemtl':
						self.current_material = values[1]
					elif values[0] == 'mtllib':
						mtl_file = os.path.join(base_path, values[1])
						self.load_mtl(mtl_file, base_path)
		except Exception as e:
			print(f"Erro ao carregar o arquivo '.obj': {e}")

	def set_material_color(self, material_name, color):
		self.override_colors[material_name] = color

	def draw(self):
		glShadeModel(GL_SMOOTH)
		current_mat = None
		for face, material in self.faces:
			if material != current_mat:
				if material in self.materials:
					if self.materials[material]['map_Kd'] and material in self.textures:
						glEnable(GL_TEXTURE_2D)
						glBindTexture(GL_TEXTURE_2D, self.textures[material])
					else:
						glDisable(GL_TEXTURE_2D)
						if material in self.override_colors:
							glColor3fv(self.override_colors[material])
						else:
							glColor3fv(self.materials[material]['Kd'])
				else:
					glDisable(GL_TEXTURE_2D)
					glColor3f(1, 1, 1)
				current_mat = material
			glBegin(GL_TRIANGLE_FAN)
			for vertex in face:
				if len(vertex) > 2 and vertex[2] > 0 and vertex[2] <= len(self.normals):
					glNormal3fv(self.normals[vertex[2] - 1])
				if len(vertex) > 1 and vertex[1] > 0 and vertex[1] <= len(self.texcoords):
					glTexCoord2fv(self.texcoords[vertex[1] - 1])
				if vertex[0] > 0 and vertex[0] <= len(self.vertices):
					glVertex3fv(self.vertices[vertex[0] - 1])
			glEnd()
		glDisable(GL_TEXTURE_2D)

	def draw_with_position(self, pos=(0, 0, 0), scale=(1, 1, 1), angle=0, axis=(0, 1, 0)):
		glPushMatrix()
		glTranslatef(*pos)
		glRotatef(angle, *axis)
		glScalef(*scale)
		self.draw()
		glPopMatrix()