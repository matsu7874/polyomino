import copy
import json
import unittest


class Polyomino:
    def __init__(self, form: list, name='#'):
        self.name = name
        self.form = copy.deepcopy(form)
        self.y_size = len(self.form)
        self.x_size = len(self.form[0])

    def __str__(self):
        return '\n'.join([''.join([self.name if self.form[y][x] else '-' for x in range(self.x_size)]) for y in range(self.y_size)])

    def rename(self, name):
        self.name = name

    def rotate(self, times=1):
        if times % 4 == 1:
            self.form = [[self.form[self.y_size - 1 - x][y]
                          for x in range(self.y_size)] for y in range(self.x_size)]
        elif times % 4 == 2:
            self.form = [[self.form[self.y_size - 1 - y][self.x_size - 1 - x]
                          for x in range(self.x_size)] for y in range(self.y_size)]
        elif times % 4 == 3:
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


def generate_variations(polyomino):
    """
    Polyomino -> List[Polyomino]
    """
    variations = set()
    p = copy.deepcopy(polyomino)
    for _rev in range(2):
        p.reverse()
        for _rot in range(4):
            p.rotate()
            f = copy.deepcopy(p.form)
            variations.add(json.dumps(f))
    return list(map(lambda f: Polyomino(f, p.name), sorted(list([json.loads(f) for f in variations]))))


def enumerate_n_omino(n: int):
    """
    Redelmeier's algorithm
    fixed（回転・反転を考慮しない）なポリオミノを列挙する。

    n=8が１秒以内に返せる現実的なラインになりそう。
    """
    if n < 1:
        return []

    UNORDER = -1
    MAX_Y = n
    MAX_X = 2 * n - 1
    X_CENTER = n - 1
    DYDX = ((1, 0), (0, 1), (-1, 0), (0, -1))

    ominos = []

    visited = [[False] * MAX_X for i in range(MAX_Y)]
    visited_queue = []
    order = [[UNORDER] * MAX_X for i in range(MAX_Y)]
    ordered_queue = []
    border = set()

    # (0,0)から探索を始める
    visited_queue.append((0, X_CENTER))
    visited[0][X_CENTER] = True
    order[0][X_CENTER] = 0

    max_visited = 0
    next_order = 1
    max_x = X_CENTER
    min_x = X_CENTER
    max_y = 0

    def dfs(y: int, x: int, last: int) -> None:
        nonlocal next_order, max_visited, ominos, max_x, min_x, max_y

        if last == 0:
            ominos.append(
                Polyomino([row[min_x:max_x + 1] for row in visited[:max_y + 1]]))
            return

        # (y, x)に隣接セルに付番する
        for dy, dx in DYDX:
            ny = y + dy
            nx = x + dx
            if (ny == 0 and nx < n) or not (0 <= ny < MAX_Y and 0 <= nx < MAX_X):
                continue
            if order[ny][nx] == UNORDER:
                order[ny][nx] = next_order
                next_order += 1
                border.add((ny, nx))
                ordered_queue.append((y, x, ny, nx))

        # セルを追加可能な箇所を列挙する
        for ny, nx in list(border):
            # if (ny == 0 and nx < n) or not (0 <= ny < MAX_Y and 0 <= nx < MAX_X):
            #     continue
            if order[ny][nx] > max_visited:
                # 深さ+1
                visited_queue.append((ny, nx))
                visited[ny][nx] = True
                pre_max_visited = max_visited
                max_visited = order[ny][nx]
                border.remove((ny, nx))

                pre_max_y = max_y
                pre_max_x = max_x
                pre_min_x = min_x
                max_y = max(max_y, ny)
                max_x = max(max_x, nx)
                min_x = min(min_x, nx)

                # 再帰
                dfs(ny, nx, last - 1)

                # 深さ-1
                # 遷移先で付番したものをキャンセルする
                while ordered_queue and (ny, nx) == (ordered_queue[-1][0], ordered_queue[-1][1]):
                    _y, _x, py, px = ordered_queue.pop()
                    order[py][px] = UNORDER
                max_y = pre_max_y
                max_x = pre_max_x
                min_x = pre_min_x
                border.add((ny, nx))
                max_visited = pre_max_visited
                visited[ny][nx] = False
                visited_queue.pop()

    dfs(0, X_CENTER, X_CENTER)

    return ominos


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
    ###
    #..
    2 2 B
    ##
    #.
    1 2 C
    ##
    ```
    """
    y_size, x_size = map(int, input().split())
    cells = []
    for _y in range(y_size):
        s = input()
        row = [s[x] == '#' for x in range(x_size)]
        cells.append(row)
    problem = Polyomino(cells, '#')

    polyominos = []
    n_polyominos = int(input())
    for i in range(n_polyominos):
        cells = []
        y_size, x_size, name = input().split()
        for y in range(int(y_size)):
            s = input()
            row = [s[x] == '#' for x in range(int(x_size))]
            cells.append(row)
        polyominos.append(Polyomino(cells, name))

    return problem, polyominos


class TestEnumerateNOmino(unittest.TestCase):
    def test_enumerate_n_polyomino(self):
        cases = ((1, 1), (2, 2), (3, 6), (4, 19), (5, 63), (6, 216),
                 (7, 760), (8, 2725), (9, 9910), (10, 36446))
        for i, expect in cases:
            with self.subTest(i=i, expect=expect):
                ominos = enumerate_n_omino(i)
                self.assertEqual(len(ominos), expect)


if __name__ == '__main__':
    unittest.main()
