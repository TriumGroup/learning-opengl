from collections import namedtuple
from random import random

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import cubes.scene_data as scene_data

class Rotation:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

class Application:
    _ROTATION_DELTA = 5
    _ROTATIONS_KEYS_MAPPINGS = {
        GLUT_KEY_RIGHT : ('y', +1),
        GLUT_KEY_LEFT : ('y', -1),
        GLUT_KEY_UP : ('x', +1),
        GLUT_KEY_DOWN : ('x', -1),
        b'z' : ('z', +1),
        b'x' : ('z', -1)
    }

    def __init__(self):
        self._colors = [(random(), random(), random()) for _ in scene_data.FACES]
        self._scene_rotation = Rotation()
        self._light_rotation = Rotation()
        self._rotations = [self._scene_rotation, self._light_rotation]
        self._current_rotation = 0
        self._lightning = True
        self._spot_light = True

        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutCreateWindow(b"Hello world!")

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_COLOR_MATERIAL)
        glEnable(GL_LIGHTING)

        self.setup_callbacks()

    def render(self):
        glMatrixMode(GL_MODELVIEW)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()

        self.setup_light()

        if self._lightning:
            self.light_transformations()
            self.draw_light()

        glLoadIdentity()

        self.scene_transformations()
        self.draw_scene()

        glFlush()
        glutSwapBuffers()

    def on_key_press(self, key, x, y):
        if key in self._ROTATIONS_KEYS_MAPPINGS:
            rotation = self._rotations[self._current_rotation]
            rotation_action = self._ROTATIONS_KEYS_MAPPINGS[key]
            coordinate, signum = rotation_action
            rotation_angle = getattr(rotation, coordinate)
            rotation_angle += self._ROTATION_DELTA * signum
            setattr(rotation, coordinate, rotation_angle)
        elif key == b'r':
            self._current_rotation = (self._current_rotation + 1) % len(self._rotations)
        elif key == b'l':
            self._lightning = not self._lightning
        elif key == b'd':
            self._spot_light = not self._spot_light
        glutPostRedisplay()
        glutPostRedisplay()

    def draw_scene(self):
        glBegin(GL_QUADS)
        for i, face in enumerate(scene_data.FACES):
            glColor3f(*self._colors[i])
            glNormal3f(*scene_data.NORMALS[i])
            for point in face:
                glVertex3f(point.x, point.y, point.z)
        glEnd()

    def rotate_transformation(self, rotation):
        glRotatef(rotation.x, 1.0, 0.0, 0.0)
        glRotatef(rotation.y, 0.0, 1.0, 0.0)
        glRotatef(rotation.z, 0.0, 0.0, 1.0)

    def scene_transformations(self):
        self.rotate_transformation(self._scene_rotation)

    def light_transformations(self):
        self.rotate_transformation(self._light_rotation)

    def draw_light(self):
        glLightfv(GL_LIGHT0, GL_POSITION, (0, 0, -1, int(self._spot_light)))

    def setup_light(self):
        if self._lightning:
            glEnable(GL_LIGHT0)
        else:
            glDisable(GL_LIGHT0)

    def setup_callbacks(self):
        glutDisplayFunc(self.render)
        glutSpecialFunc(self.on_key_press)
        glutKeyboardFunc(self.on_key_press)

    def start(self):
        glutMainLoop()
