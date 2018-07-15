"""
DancingLinks
Exact Cover Problemを効率的に解くKnuth's Algorithm Xの効率的な実装
"""

import unittest
import sys

sys.setrecursionlimit(10000)


class Node:
    def __init__(self, row_index, column_index):
        self.row_index = row_index
        self.column_index = column_index
        self.head = self
        self.up = self
        self.down = self
        self.left = self
        self.right = self

    def __str__(self):
        return 'node' + str((self.row_index, self.column_index))


class Header(Node):
    """
    columnのheader
    """

    def __init__(self, row_index, column_index):
        super().__init__(row_index, column_index)
        self.size = 0

    def __str__(self):
        return 'header' + str((self.row_index, self.column_index, self.size))


class DancingLinks:
    """
    上下左右にNodeが連なったデータ構造

    行数: |subsets|
    列数: |collection_size|
    """

    def __init__(self, collection_size, subsets):
        self.n = collection_size
        self.m = len(subsets)

        self.head = Header(-1, -1)
        self.headers = []
        for column_index in range(collection_size):
            header = Header(-1, column_index)
            self.insert_header(header)
            self.headers.append(header)

        for row_index, row in enumerate(subsets):
            if not row:
                continue

            row_header = Node(row_index, row[0])
            column_header = self.headers[row[0]]
            self.insert_to_column(column_header, row_header)

            for column_index in row[1:]:
                node = Node(row_index, column_index)
                column_header = self.headers[column_index]
                self.insert_to_column(column_header, node)
                self.insert_to_row(row_header, node)

    def __str__(self):
        """O(nm)なので注意
        """

        cells = [[False for j in range(self.n)] for i in range(self.m)]
        node = self.head.right
        while node is not self.head:
            column_node = node.down
            while column_node is not node:
                cells[column_node.row_index][column_node.column_index] = True
                column_node = column_node.down
            node = node.right
        return '\n'.join([''.join(['O' if x else '-' for x in row]) for row in cells])

    def insert_header(self, header):
        """headerをheadの行に追加する。
        """
        header.right = self.head
        header.left = self.head.left
        self.head.left.right = header
        self.head.left = header

    def insert_to_row(self, row_header, node):
        """行にノードを追加する。
        """
        node.right = row_header
        node.left = row_header.left
        row_header.left.right = node
        row_header.left = node

    def insert_to_column(self, column_header, node):
        """列にノードを追加する。
        """
        column_header.size += 1
        node.head = column_header

        node.up = column_header.up
        node.down = column_header
        column_header.up.down = node
        column_header.up = node

    def cover(self, selected_node):
        """
        selected_nodeを含む行を選択する。
        """
        node = selected_node
        while True:
            # column_headerをheadから外す
            header = node.head
            header.left.right = header.right
            header.right.left = header.left

            column_node = header.down
            while column_node is not header:
                # 選べなくなる要素を列から外していく
                row_node = column_node.right
                while row_node is not column_node:
                    row_node.up.down = row_node.down
                    row_node.down.up = row_node.up
                    row_node.head.size -= 1
                    row_node = row_node.right
                column_node = column_node.down
            node = node.right
            if node is selected_node:
                break

    def uncover(self, selected_node):
        """
        selected_nodeを含む行を選択解除する。
        """

        node = selected_node
        while True:
            # column_headerをheadつなげる
            header = node.head
            header.left.right = header
            header.right.left = header

            column_node = header.down
            while column_node is not header:
                row_node = column_node.right
                while row_node is not column_node:
                    row_node.up.down = row_node
                    row_node.down.up = row_node
                    row_node.head.size += 1
                    row_node = row_node.right
                column_node = column_node.down
            node = node.right
            if node is selected_node:
                break

    def is_empty(self):
        return self.head.right is self.head

    def algorithm_x(self):
        """solves exact cover problem

        algorithm_x() -> List[List[int]]
        Exact Coverの部分集合のインデックス列を返す。
        """
        result = []

        def _algorithm_x(sss):
            if self.is_empty():
                result.append(set(sss))
            else:
                # 列の選択
                min_header = self.head.right

                header = min_header
                while header is not self.head:
                    # 埋めることができない要素がある場合はpopする
                    if header.size == 0:
                        return None
                    if header.size < min_header.size:
                        min_header = header
                    header = header.right

                column_node = min_header.down
                while column_node is not min_header:
                    self.cover(column_node)
                    sss.append(column_node.row_index)
                    _algorithm_x(sss)
                    sss.pop()
                    self.uncover(column_node)
                    column_node = column_node.down

        _algorithm_x([])
        return result


class TestDancingLinks(unittest.TestCase):
    def test_algorithm_x(self):
        collection = [0, 1, 2, 3, 4]
        subsets = [
            [0, 2],
            [0, 3, 4],
            [1, 3],
            [1, 4],
            [2, 3],
            [4],
        ]
        dl = DancingLinks(len(collection), subsets)

        result = dl.algorithm_x()
        self.assertEqual(result, [set([0, 2, 5])])

        collection = [0, 1, 2]
        subsets = [
            [0],
            [1],
            [0, 1],
            [2],
        ]
        dl = DancingLinks(len(collection), subsets)

        result = dl.algorithm_x()
        self.assertEqual(result, [set([0, 1, 3]), set([2, 3])])

        collection = [0]
        subsets = [
            [0],
            [0],
            [0],
        ]
        dl = DancingLinks(len(collection), subsets)

        result = dl.algorithm_x()
        self.assertEqual(result, [set([0]), set([1]), set([2])])


if __name__ == '__main__':
    unittest.main()
