import copy
import json
import time

import dancinglinks


class Polyomino:
    def __init__(self, form, name='-'):
        self.name = name
        self.form = copy.deepcopy(form)
        self.y_size = len(self.form)
        self.x_size = len(self.form[0])

    def __str__(self):
        return '\n'.join([''.join([self.name if self.form[y][x] else '-' for x in range(self.x_size)]) for y in range(self.y_size)])

    def rename(self, name):
        self.name = name

    def rotate(self, times=1):
        if times == 1:
            self.form = [[self.form[self.y_size - 1 - x][y]
                          for x in range(self.y_size)] for y in range(self.x_size)]
        elif times == 2:
            self.form = [[self.form[self.y_size - 1 - y][self.x_size - 1 - x]
                          for x in range(self.x_size)] for y in range(self.y_size)]
        elif times == 3:
            self.form = [[self.form[x][self.x_size - 1 - y]
                          for x in range(self.y_size)] for y in range(self.x_size)]

        self.y_size = len(self.form)
        self.x_size = len(self.form[0])

    def reverse(self):
        reversed_form = [[False for j in range(
            self.x_size)] for i in range(self.y_size)]
        for y in range(self.y_size):
            for x in range(self.x_size):
                reversed_form[y][self.x_size - 1 - x] = self.form[y][x]
        self.form = reversed_form

    def generate_variations(self):
        """
        () -> List[Polyomino]
        """
        variations = set()
        p = copy.deepcopy(self)
        for _rev in range(2):
            p.reverse()
            for _rot in range(4):
                p.rotate()
                f = copy.deepcopy(p.form)
                variations.add(json.dumps(f))
        return list(map(lambda f: Polyomino(f, self.name), sorted(list([json.loads(f) for f in variations]))))

    def can_add_polyomino(self, polyomino, offset_y, offset_x):
        if polyomino.y_size + offset_y > self.y_size:
            return False
        if polyomino.x_size + offset_x > self.x_size:
            return False

        for i in range(polyomino.y_size):
            for j in range(polyomino.x_size):
                if polyomino.form[i][j] and self.form[i + offset_y][j + offset_x]:
                    return False
        return True

    def add_polyomino(self, polyomino, offset_y, offset_x):
        for y in range(polyomino.y_size):
            for x in range(polyomino.x_size):
                self.form[offset_y + y][offset_x + x] |= polyomino.form[y][x]

    def remove_polyomino(self, polyomino, offset_y, offset_x):
        for y in range(polyomino.y_size):
            for x in range(polyomino.x_size):
                self.form[offset_y + y][offset_x +
                                        x] &= not polyomino.form[y][x]


def read_puzzle_2d():
    """
    入力は下記の形式で与えられる
    ```
    3 3
    ---
    ---
    ---
    3
    2 3 A
    ooo
    o..
    2 2 B
    oo
    o.
    1 2 C
    oo
    ```
    """
    y_size, x_size = map(int, input().split())
    cells = []
    for _y in range(y_size):
        s = input()
        row = [s[x] == 'o' for x in range(x_size)]
        cells.append(row)
    problem = Polyomino(cells, '#')

    polyominos = []
    n_polyominos = int(input())
    for i in range(n_polyominos):
        cells = []
        y_size, x_size, name = input().split()
        for y in range(int(y_size)):
            s = input()
            row = [s[x] == 'o' for x in range(int(x_size))]
            cells.append(row)
        polyominos.append(Polyomino(cells, name))

    return problem, polyominos
