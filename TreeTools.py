import random
import math

import numpy


class Genome:
    length = 0  # ok
    length_dev = 1  # ok
    size = 2  # ok
    size_cng = 3  # ok
    size_from_ancestor = 4  # 0 - 100
    size_from_level = 5  # 0 - 100
    red = 6  # ok
    green = 7  # ok
    blue = 8  # ok
    red_cng = 9  # ok
    green_cng = 10  # ok
    blue_cng = 11  # ok
    color_from_ancestor = 12  # 0 - 100
    color_dev = 13  # ok
    num_of_branches = 14  # 1 - 3
    angles_of_branches = 15  # ok
    angle_dev = 16  # ok
    turn = 17  # ok
    rand_turn = 18  # ok
    down_up = 19  # ok

    def __init__(self, array: numpy.array):
        self.genome: numpy.array = array

    def __getitem__(self, item):
        return self.genome[item]

    def copy(self):
        return Genome(self.genome.copy())


class Agent:
    def __init__(self, canvas, gen: numpy.array, x: int, y: int, turn: int, r_anc: int,
                 g_anc: int, b_anc: int, size_anc: int, size_lvl: int):
        self.canvas = canvas
        self.genome_level = gen
        self.turn: int = turn
        self.r_anc: int = r_anc
        self.g_anc: int = g_anc
        self.b_anc: int = b_anc
        self.size_anc: int = size_anc
        self.size_lvl: int = size_lvl
        self.x: int = x
        self.y: int = y
        self.items = []

    @staticmethod
    def __from_ancestor(anc, gen, frm):
        return anc * frm / 100 + gen * (100 - frm) / 100

    def __color_dev(self, color):
        return color + random.random() * 2 * self.genome_level[Genome.color_dev] - self.genome_level[Genome.color_dev]

    def __cr(self, x: int, y: int, d: int, color: str):
        return self.canvas.create_oval(x - d / 2, y - d / 2, x + d / 2, y + d / 2, fill=color, width=0)

    def render(self):
        length = self.genome_level[Genome.length] + random.randint(-int(self.genome_level[Genome.length_dev]),
                                                                   int(self.genome_level[Genome.length_dev]))
        r = self.__color_dev(
            self.__from_ancestor(self.r_anc, self.genome_level[Genome.red],
                                 self.genome_level[Genome.color_from_ancestor]))
        g = self.__color_dev(self.__from_ancestor(self.g_anc, self.genome_level[Genome.green],
                                                  self.genome_level[Genome.color_from_ancestor]))
        b = self.__color_dev(
            self.__from_ancestor(self.b_anc, self.genome_level[Genome.blue],
                                 self.genome_level[Genome.color_from_ancestor]))
        self.turn += random.random() * 2 * self.genome_level[Genome.angle_dev] - self.genome_level[Genome.angle_dev]
        size = self.__from_ancestor(self.size_anc, self.genome_level[Genome.size],
                                    self.genome_level[Genome.size_from_ancestor])
        size = self.__from_ancestor(self.size_lvl, size, self.genome_level[Genome.size_from_level])
        dwn = 2 / (1 + 2.718 ** (-self.genome_level[Genome.down_up] / 1000)) - 1
        for _ in range(int(length)):
            self.turn += random.random() * 2 * self.genome_level[Genome.rand_turn] \
                         - self.genome_level[Genome.rand_turn] + self.genome_level[Genome.turn]
            if dwn >= 0:
                self.turn = 180 * dwn + self.turn * (1 - dwn)
            else:
                self.turn = self.turn * (dwn + 1)
            self.x += math.sin(self.turn * 0.0175)
            self.y -= math.cos(self.turn * 0.0175)
            size += self.genome_level[Genome.size_cng] / 100
            size = max(size, 5)
            r += self.genome_level[Genome.red_cng]
            g += self.genome_level[Genome.green_cng]
            b += self.genome_level[Genome.blue_cng]
            self.items.append(self.__cr(self.x, self.y, int(size), '#%02x%02x%02x' %
                                        (max(min(int(r), 255), 0), max(min(int(g), 255), 0), max(min(int(b), 255), 0))))
        return self.x, self.y, self.turn, r, g, b, size


class Tree:
    def __init__(self, canvas, genome: Genome, x, y, turn=0, r=127, g=127, b=127, size=10, sizes_levels=None, n=0):
        if sizes_levels is None:
            sizes_levels = []
        if n >= genome.genome.shape[1]:
            self.items = []
            return
        self.canvas = canvas
        root_agent = Agent(canvas, genome[:, n], x, y, turn, r, g, b, size, sizes_levels[n])
        end_x, end_y, end_turn, end_r, end_g, end_b, end_size = root_agent.render()
        self.items: list[int] = root_agent.items
        angle = genome[Genome.angles_of_branches, n]
        if genome[Genome.num_of_branches, n] == 1:
            self.items += Tree(canvas, genome, end_x, end_y, end_turn, end_r, end_g, end_b, end_size, sizes_levels,
                               n + 1).items
        elif genome[Genome.num_of_branches, n] == 2:
            self.items += Tree(canvas, genome, end_x, end_y, end_turn + angle, end_r, end_g, end_b, end_size,
                               sizes_levels, n + 1).items
            self.items += Tree(canvas, genome, end_x, end_y, end_turn - angle, end_r, end_g, end_b, end_size,
                               sizes_levels, n + 1).items
        elif genome[Genome.num_of_branches, n] == 3:
            self.items += Tree(canvas, genome, end_x, end_y, end_turn + angle, end_r, end_g, end_b, end_size,
                               sizes_levels, n + 1).items
            self.items += Tree(canvas, genome, end_x, end_y, end_turn, end_r, end_g, end_b, end_size, sizes_levels,
                               n + 1).items
            self.items += Tree(canvas, genome, end_x, end_y, end_turn - angle, end_r, end_g, end_b, end_size,
                               sizes_levels, n + 1).items

    def delete(self):
        for elem in self.items:
            self.canvas.delete(elem)


def rand_gen(a, b, n):
    return [random.random() * (a - b) + b for _ in range(n)]


def rand_gen_int(a, b, n):
    return [random.randint(a, b) for _ in range(n)]


def rand_genome(n=8) -> Genome:
    return Genome(numpy.array([
        rand_gen(50, 120, n),  # length
        rand_gen(0, 10, n),  # length_dev
        rand_gen(9, 13, n),  # size
        rand_gen(-12, 12, n),  # size_cng
        [0] + rand_gen(0, 70, n-1),  # size_from_ancestor
        rand_gen(10, 20, n),  # size_from_level
        rand_gen(30, 240, n),  # red
        rand_gen(30, 240, n),  # green
        rand_gen(30, 240, n),  # blue
        rand_gen(-2, 2, n),  # red_cng
        rand_gen(-2, 2, n),  # green_cng
        rand_gen(-2, 2, n),  # blue_cng
        [0] + rand_gen(20, 60, n-1),  # color_from_ancestor
        rand_gen(-70, 70, n),  # color_dev
        [random.choices([1, 2, 3], weights=[0.2, 0.4, 0.4], k=1)[0] for _ in range(n)],  # num_of_branches
        rand_gen(30, 90, n),  # angles_of_branches
        rand_gen(0, 15, n),  # angle_dev
        rand_gen(-1., 1.5, n),  # turn
        rand_gen(0, 6, n),  # rand_turn
        rand_gen(-25, 1, n),  # down_up
    ]))


def interbreed(a: Genome, b: Genome):
    return numpy.array([
        [random.choice([item1, item2]) for item1, item2 in zip(row1, row2)]
        for row1, row2 in zip(list(a.genome), list(b.genome))])


def add_mut(a: Genome):
    row, column = a.genome.shape
    row = random.randint(0, row)
    column = random.randint(0, column)
    b = a.genome.copy()
    b[row, column] = rand_genome(1).genome[row, 0]
    return Genome(b)


def interbreed_with_mut(a: Genome, b: Genome):
    return add_mut(Genome(numpy.array([
        [random.choice([item1, item2]) for item1, item2 in zip(row1, row2)]
        for row1, row2 in zip(list(a.genome), list(b.genome))])))


def create_tree(canvas, genome: Genome, x: int = 800, y: int = 600, sizes_levels: list = None) -> Tree:
    if sizes_levels is None:
        sizes_levels = [13, 12, 11, 10, 9, 8, 7, 6]
    return Tree(canvas, genome, x, y, sizes_levels=sizes_levels)


def delete(tree: Tree) -> None:
    tree.delete()


def zero_gen(n):
    return Genome(numpy.zeros((20, n)))
