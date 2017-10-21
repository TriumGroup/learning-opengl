from collections import namedtuple

Point = namedtuple('Point', ['x', 'y', 'z'])

_EDGE_LENGTH = 0.5

_POINTS = [
    Point(0, 0, 0),
    Point(_EDGE_LENGTH, 0, 0),
    Point(_EDGE_LENGTH, -_EDGE_LENGTH, 0),
    Point(0, -_EDGE_LENGTH, 0),
    Point(0, 0, -_EDGE_LENGTH),
    Point(_EDGE_LENGTH, 0, -_EDGE_LENGTH),
    Point(_EDGE_LENGTH, -_EDGE_LENGTH, -_EDGE_LENGTH),
    Point(0, -_EDGE_LENGTH, -_EDGE_LENGTH),
    Point(0, 0, _EDGE_LENGTH),
    Point(0, -_EDGE_LENGTH, _EDGE_LENGTH),
    Point(-_EDGE_LENGTH, -_EDGE_LENGTH, _EDGE_LENGTH),
    Point(-_EDGE_LENGTH, 0, _EDGE_LENGTH),
    Point(-_EDGE_LENGTH, 0, 0),
    Point(-_EDGE_LENGTH, -_EDGE_LENGTH, 0),
    Point(-_EDGE_LENGTH, _EDGE_LENGTH, 0),
    Point(0, _EDGE_LENGTH, 0),
    Point(-_EDGE_LENGTH, 0, -_EDGE_LENGTH),
    Point(-_EDGE_LENGTH, _EDGE_LENGTH, -_EDGE_LENGTH),
    Point(0, _EDGE_LENGTH, -_EDGE_LENGTH)
]

_FACES_DESCRIPTION = [
    [0, 1, 2, 3],
    [0, 1, 5, 4],
    [1, 2, 6, 5],
    [2, 3, 7, 6],
    [3, 0, 4, 7],
    [4, 5, 6, 7],
    [11, 8, 9, 10],
    [11, 8, 0, 12],
    [8, 9, 3, 0],
    [9, 10, 13, 3],
    [10, 11, 12, 13],
    [12, 0, 3, 13],
    [14, 15, 0, 12],
    [14, 15, 18, 17],
    [15, 0, 4, 18],
    [0, 12, 16, 4],
    [12, 14, 17, 16],
    [17, 18, 4, 16]
]

FACES = [tuple((_POINTS[i] for i in face)) for face in _FACES_DESCRIPTION]
