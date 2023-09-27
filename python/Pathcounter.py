from z3 import *

class PathCounter:
    def __init__(
        self, size_x, size_y, obstacles, steps, start_x, start_y, finish_x, finish_y
    ):
        self.goal = Goal()

        self.size_x = size_x
        self.size_y = size_y
        self.obstacles = obstacles
        self.start_x = start_x
        self.start_y = start_y
        self.finish_x = finish_x
        self.finish_y = finish_y
        self.steps = steps

        self.visit = [
            [
                [Bool("x_{}_{}_{}".format(k, i, j)) for j in range(size_x)]
                for i in range(size_y)
            ]
            for k in range(steps + 1)
        ]

        self.north = [
            [
                [Bool("n_{}_{}_{}".format(k, i, j)) for j in range(size_x)]
                for i in range(size_y)
            ]
            for k in range(steps + 1)
        ]

        self.east = [
            [
                [Bool("e_{}_{}_{}".format(k, i, j)) for j in range(size_x)]
                for i in range(size_y)
            ]
            for k in range(steps + 1)
        ]

        self.south = [
            [
                [Bool("s_{}_{}_{}".format(k, i, j)) for j in range(size_x)]
                for i in range(size_y)
            ]
            for k in range(steps + 1)
        ]

        self.west = [
            [
                [Bool("w_{}_{}_{}".format(k, i, j)) for j in range(size_x)]
                for i in range(size_y)
            ]
            for k in range(steps + 1)
        ]

        self.goal.add(self.start())
        self.goal.add(self.finish())
        self.goal.add(self.dont_visit_obstacles())
        self.goal.add(self.direction_if_visit())
        self.goal.add(self.stay_in_grid())
        self.goal.add(self.follow_direction())
        self.goal.add(self.every_step())

        t = Tactic("tseitin-cnf")
        expr = t(self.goal)

        self.dimacs = expr[0].dimacs()

    def start(self):
        return self.visit[0][self.start_y][self.start_x]

    def finish(self):
        clause = []
        for k in range(self.steps):
            term = Implies(
                self.visit[k][self.finish_y][self.finish_x],
                self.visit[k + 1][self.finish_y][self.finish_x],
            )
            clause.append(term)

        term = Or(
            [self.visit[k][self.finish_y][self.finish_x] for k in range(self.steps + 1)]
        )
        clause.append(term)
        return clause

    def dont_visit_obstacles(self):
        return [
            Not(self.visit[k][i][j])
            for (j, i) in self.obstacles
            for k in range(self.steps)
        ]

    def direction_if_visit(self):
        clause = []
        for k in range(self.steps):
            for i in range(self.size_y):
                for j in range(self.size_x):
                    term_visit = Implies(
                        (self.visit[k][i][j]),
                        Or(
                            self.north[k][i][j],
                            self.east[k][i][j],
                            self.south[k][i][j],
                            self.west[k][i][j],
                        ),
                    )
                    clause.append(term_visit)
        return clause

    def stay_in_grid(self):
        clause = []
        for k in range(self.steps):
            for i in range(self.size_y):
                term_left = Not(self.west[k][i][0])
                term_right = Not(self.east[k][i][self.size_x - 1])
                clause.append(term_left)
                clause.append(term_right)

            for j in range(self.size_x):
                term_top = Not(self.north[k][0][j])
                term_bottom = Not(self.south[k][self.size_y - 1][j])
                clause.append(term_top)
                clause.append(term_bottom)
        return clause

    def follow_direction(self):
        clause = []
        for k in range(self.steps):
            for i in range(self.size_y):
                for j in range(self.size_x):
                    if i != self.finish_y or j != self.finish_x:
                        if i > 0:
                            term_go_up = Or(
                                Not(self.north[k][i][j]), self.visit[k + 1][i - 1][j]
                            )
                            clause.append(term_go_up)
                        if j < self.size_x - 1:
                            term_go_right = Or(
                                Not(self.east[k][i][j]), self.visit[k + 1][i][j + 1]
                            )
                            clause.append(term_go_right)
                        if i < self.size_y - 1:
                            term_go_down = Or(
                                Not(self.south[k][i][j]), self.visit[k + 1][i + 1][j]
                            )
                            clause.append(term_go_down)
                        if j > 0:
                            term_go_left = Or(
                                Not(self.west[k][i][j]), self.visit[k + 1][i][j - 1]
                            )
                            clause.append(term_go_left)
        return clause

    def every_step(self):
        term = []

        for k in range(self.steps + 1):
            coordinate_pairs = [
                (i, j) for i in range(self.size_y) for j in range(self.size_x)
            ]

            for i1, j1 in coordinate_pairs:
                for i2, j2 in coordinate_pairs:
                    if i1 != i2 or j1 != j2:
                        clause_and = And(self.visit[k][i1][j1], self.visit[k][i2][j2])
                        term.append(Not(clause_and))

            clause_sum = Or([self.visit[k][i][j] for i, j in coordinate_pairs])
            term.append(clause_sum)

        return term