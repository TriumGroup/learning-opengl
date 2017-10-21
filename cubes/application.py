from collections import namedtuple
from random import random

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import cubes.scene_data as scene_data

def signum(x):
    return 1 if x >= 0 else -1

class Application:
    _LIGHTS = [
        (0, 0, -1, 1),
        (1, 0, 0, 1),
        (0, 1, 0, 1),
    ]

    def __init__(self):
        self._colors = [(random(), random(), random()) for _ in scene_data.FACES]
        self._rotate_y = 0
        self._rotate_x = 0
        self._rotate_z = 0
        self._light_mode = 0

        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutCreateWindow(b"Hello world!")

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)

        self.setup_callbacks()

    def render(self):
        print(self._LIGHTS[self._light_mode])
        glMatrixMode(GL_MODELVIEW)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()

        self.transformations()
        self.draw_scene()

        glLoadIdentity()

        self.set_light()

        glFlush()
        glutSwapBuffers()

    def on_key_press(self, key, x, y):
        if key == GLUT_KEY_RIGHT:
            self._rotate_y += 5
        elif key == GLUT_KEY_LEFT:
            self._rotate_y -= 5
        elif key == GLUT_KEY_UP:
            self._rotate_x += 5
        elif key == GLUT_KEY_DOWN:
            self._rotate_x -= 5
        elif key == b'z':
            self._rotate_z += 5
        elif key == b'x':
            self._rotate_z -= 5
        elif key == b'l':
            print(self._LIGHTS[self._light_mode])
            self._light_mode = (self._light_mode + 1) % len(self._LIGHTS)
            print(self._LIGHTS[self._light_mode])
        glutPostRedisplay()

    def draw_scene(self):
        glBegin(GL_QUADS)
        for i, face in enumerate(scene_data.FACES):
            glColor3f(*self._colors[i])
            glNormal3f(*scene_data.NORMALS[i])
            for point in face:
                glVertex3f(point.x, point.y, point.z)
        glEnd()

    def transformations(self):
        glRotatef(self._rotate_x, 1.0, 0.0, 0.0)
        glRotatef(self._rotate_y, 0.0, 1.0, 0.0)
        glRotatef(self._rotate_z, 0.0, 0.0, 1.0)

    def set_light(self):
        glLight(GL_LIGHT0, GL_POSITION, self._LIGHTS[self._light_mode])


    def setup_callbacks(self):
        glutDisplayFunc(self.render)
        glutSpecialFunc(self.on_key_press)
        glutKeyboardFunc(self.on_key_press)

    def start(self):
        glutMainLoop()
