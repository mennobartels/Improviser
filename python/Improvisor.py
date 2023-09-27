from Pathcounter import *
from pyapproxmc import Counter
import random
import csv
import math


def approxmc_count_projected(dimacs, eps):
    s = Counter(epsilon=eps)

    lines = dimacs.split("\n")
    clauses = []
    for line in lines:
        if not line.startswith("c") and not line.startswith("p"):
            elements = line.split(" ")[:-1]
            int_elements = [int(element) for element in elements]
            clauses.append(int_elements)

    for clause in clauses:
        if len(clause) > 0:
            s.add_clause(clause)

    projection_set = []

    for line in lines:
        if "x_" in line:
            words = line.split()
            number = int(words[1])
            projection_set.append(number)

    cells, hashes = s.count(projection_set)
    count_average = cells * 2**hashes
    count_min = (count_average / (1 + eps))
    count_max = (count_average * (1 + eps))
    return count_average, count_min, count_max


def parse_csv(filename):
    grid = []
    with open(filename, "r") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            grid.append(list(row))

    # Calculate dimensions
    size_x = len(grid[0])
    size_y = len(grid)

    # Find coordinates of S, F, and list of W
    start_coords = None
    finish_coords = None
    obstacles = []

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == "S":
                start_coords = (x, y)
            elif cell == "F":
                finish_coords = (x, y)
            elif cell == "W":
                obstacles.append((x, y))

    return {
        "size_x": size_x,
        "size_y": size_y,
        "start_coords": start_coords,
        "finish_coords": finish_coords,
        "obstacles": obstacles,
    }


def scale_weights(weights):
    total = sum(weights)
    scaled_weights = [w / total for w in weights]
    return scaled_weights


class Improvisor:
    def __init__(self, csv, steps, lam=0, eps=0.8, show=False):
        grid_info = parse_csv(csv)

        # Initialize attributes based on parsed information
        self.size_x = grid_info["size_x"]
        self.size_y = grid_info["size_y"]
        self.obstacles = grid_info["obstacles"]
        self.total_steps = steps
        self.start_x = grid_info["start_coords"][0]
        self.start_y = grid_info["start_coords"][1]
        self.finish_x = grid_info["finish_coords"][0]
        self.finish_y = grid_info["finish_coords"][1]
        self.current_start_x = self.start_x
        self.current_start_y = self.start_y
        self.current_steps = steps - 1
        self.lam = lam
        self.eps = eps
        self.current_eps = eps
        self.show = show

        self.path = []

    def improvise(self):
        while not (
            self.current_start_x == self.finish_x
            and self.current_start_y == self.finish_y
        ):
            if self.current_steps < 0:
                print("goal not reached")
                break

            total_paths = 0
            paths_right = 0
            paths_down = 0
            paths_left = 0
            paths_up = 0
            weights = []
            next_locs = []
            
            r_min, r_max, d_min, d_max, l_min, l_max, u_min, u_max = 0,0,0,0,0,0,0,0

            if self.size_x > self.current_start_x + 1:
                if (
                    self.current_start_x + 1,
                    self.current_start_y,
                ) not in self.obstacles:
                    counter = PathCounter(
                        self.size_x,
                        self.size_y,
                        self.obstacles,
                        self.current_steps,
                        self.current_start_x + 1,
                        self.current_start_y,
                        self.finish_x,
                        self.finish_y,
                    )
                    dimacs = counter.dimacs

                    paths_right, r_min, r_max = approxmc_count_projected(dimacs, self.current_eps)
                    if self.show:
                        print("right: {}".format(paths_right))
                    if paths_right:
                        total_paths += paths_right
                        next_locs.append("r")
                elif self.show:
                    print("right: Obstacle")

            if self.size_y > self.current_start_y + 1:
                if (
                    self.current_start_x,
                    self.current_start_y + 1,
                ) not in self.obstacles:
                    counter = PathCounter(
                        self.size_x,
                        self.size_y,
                        self.obstacles,
                        self.current_steps,
                        self.current_start_x,
                        self.current_start_y + 1,
                        self.finish_x,
                        self.finish_y,
                    )
                    dimacs = counter.dimacs

                    paths_down, d_min, d_max  = approxmc_count_projected(dimacs, self.current_eps)
                    if self.show:
                        print("down: {}".format(paths_down))
                    if paths_down:
                        total_paths += paths_down
                        next_locs.append("d")
                elif self.show:
                    print("down: Obstacle")

            if self.current_start_x > 0:
                if (
                    self.current_start_x - 1,
                    self.current_start_y,
                ) not in self.obstacles:
                    counter = PathCounter(
                        self.size_x,
                        self.size_y,
                        self.obstacles,
                        self.current_steps,
                        self.current_start_x - 1,
                        self.current_start_y,
                        self.finish_x,
                        self.finish_y,
                    )
                    dimacs = counter.dimacs

                    paths_left, l_min, l_max  = approxmc_count_projected(dimacs, self.current_eps)
                    if self.show:
                        print("left: {}".format(paths_left))
                    if paths_left:
                        total_paths += paths_left
                        next_locs.append("l")
                elif self.show:
                    print("left: Obstacle")

            if self.current_start_y > 0:
                if (
                    self.current_start_x,
                    self.current_start_y - 1,
                ) not in self.obstacles:
                    counter = PathCounter(
                        self.size_x,
                        self.size_y,
                        self.obstacles,
                        self.current_steps,
                        self.current_start_x,
                        self.current_start_y - 1,
                        self.finish_x,
                        self.finish_y,
                    )
                    dimacs = counter.dimacs

                    paths_up, u_min, u_max = approxmc_count_projected(dimacs, self.current_eps)
                    if self.show:
                        print("up: {}".format(paths_up))
                    if paths_up:
                        total_paths += paths_up
                        next_locs.append("u")
                elif self.show:
                    print("up: Obstacle")

            min_total_paths = r_min + d_min + l_min + u_min
            max_total_paths = r_max + d_max + l_max + u_max

            maxes = [(r_min/(r_min + d_max + l_max + u_max)),
                     (d_min/(r_max + d_min + l_max + u_max)),
                     (l_min/(r_max + d_max + l_min + u_max)),
                     (u_min/(r_max + d_max + l_max + u_min))]
            max_lams = []
            for i in maxes:
                if i != 0:
                    max_lams.append(i)

            max_lam = min(max_lams)
            if self.show:
                print("total paths: {}".format(total_paths))
                print("epsilon: current_eps = {}, eps = {}".format(self.current_eps, self.eps))

                print("for this eps lambda should be: \nlam < {}".format(1 / total_paths))

            if self.lam > 1 / total_paths:
                print("No improvisor possible")
                break
            
            if paths_right:
                prob_right = paths_right / total_paths

                # print("-------------right-----------------")
                # print("r min {}".format(r_min))
                # print("d max {}".format(d_max))
                # print("u max {}".format(u_max))
                # print("l max {}".format(l_max))
                # # print((r_min/(r_min + d_max + l_max + u_max)))
                # print(prob_right) 
                # print("r max {}".format(r_max))
                # print("d min {}".format(d_min))
                # print("u min {}".format(u_min))
                # print("l min {}".format(l_min))
                # print((r_max/(r_max + d_min + l_min + u_min)))
                # print("------------------------------")

                if self.lam > (r_max/(r_max + d_min + l_min + u_min)):
                    if self.show:
                        print("No improvisor right")
                    next_locs.remove("r")
                elif (r_min/(r_min + d_max + l_max + u_max)) <= self.lam and self.lam <= (r_max/(r_max + d_min + l_min + u_min)):
                    if self.current_eps < 0.01:
                        if self.show:
                            print("No improvisor found right")
                        next_locs.remove("r")
                    else:
                        if self.show:
                            print("Uncertain about improvisor right, make eps smaller")
                        self.current_eps /= 2
                        continue
                else:
                    weights.append(prob_right)

            if paths_down:
                prob_down = paths_down / total_paths

                # print("-------------down-----------------")
                # # print((d_min/(r_max + d_min + l_max + u_max)))
                # print(prob_down) 
                # # print((d_max/(r_min + d_max + l_min + u_min)))
                # print("------------------------------")

                if self.lam > (d_max/(r_min + d_max + l_min + u_min)):
                    if self.show:
                        print("No improvisor down")
                    next_locs.remove("d")
                elif (d_min/(r_max + d_min + l_max + u_max)) <= self.lam and self.lam <= (d_max/(r_min + d_max + l_min + u_min)):
                    if self.current_eps < 0.01:
                        if self.show:
                            print("No improvisor found down")
                        next_locs.remove("d")
                    else:
                        if self.show:
                            print("Uncertain about improvisor down, make eps smaller")
                        self.current_eps /= 2
                        continue
                else:
                    weights.append(prob_down)

            if paths_left:
                prob_left = paths_left / total_paths

                # print("-------------left-----------------")
                # print((l_min/(r_max + d_max + l_min + u_max)))
                # print(self.lam) 
                # print((l_max/(r_min + d_min + l_max + u_min)))
                # print("------------------------------")


                if self.lam > (l_max/(r_min + d_min + l_max + u_min)):
                    if self.show:
                        print("No improvisor left")
                    next_locs.remove("l")
                elif (l_min/(r_max + d_max + l_min + u_max)) <= self.lam and self.lam <= (l_max/(r_min + d_min + l_max + u_min)):
                    if self.current_eps < 0.01:
                        if self.show:
                            print("No improvisor found left")
                        next_locs.remove("l")
                    else:
                        if self.show:
                            print("Uncertain about improvisor left, make eps smaller")
                        self.current_eps /= 2
                        continue
                else:
                    weights.append(prob_left)

            if paths_up:
                prob_up = paths_up / total_paths

                # print("-------------left-----------------")
                # # print((u_min/(r_max + d_max + l_max + u_min)))
                # print(prob_up) 
                # # print((u_max/(r_min + d_min + l_min + u_max)))
                # print("------------------------------")

                if self.lam > (u_max/(r_min + d_min + l_min + u_max)):
                    if self.show:
                        print("No improvisor up")
                    next_locs.remove("u")
                elif (u_min/(r_max + d_max + l_max + u_min)) <= self.lam and self.lam <= (u_max/(r_min + d_min + l_min + u_max)):
                    if self.current_eps < 0.01:
                        if self.show:
                            print("No improvisor found up")
                        next_locs.remove("u")
                    else:
                        if self.show:
                            print("Uncertain about improvisor up, make eps smaller")
                        self.current_eps /= 2
                        continue
                else:
                    weights.append(prob_up)

            if next_locs:
                next = random.choices(next_locs, weights, k=1)[0]
            else:
                break

            if self.show:
                print(next_locs)
                print(weights)

            if next == "r":
                self.lam = self.lam * (1 / prob_right)
                self.current_start_x += 1
                self.current_steps -= 1
                if self.show:
                    print(
                        "chose right at step {}".format(
                            self.total_steps - self.current_steps - 1
                        )
                    )
                self.path.append(next)

            if next == "d":
                self.lam = self.lam * (1 / prob_down)
                self.current_start_y += 1
                self.current_steps -= 1
                if self.show:
                    print(
                        "chose down at step {}".format(
                            self.total_steps - self.current_steps - 1
                        )
                    )
                self.path.append(next)

            if next == "l":
                self.lam = self.lam * (1 / prob_left)
                self.current_start_x -= 1
                self.current_steps -= 1
                if self.show:
                    print(
                        "chose left at step {}".format(
                            self.total_steps - self.current_steps - 1
                        )
                    )
                self.path.append(next)

            if next == "u":
                self.lam = self.lam * (1 / prob_up)
                self.current_start_y -= 1
                self.current_steps -= 1
                if self.show:
                    print(
                        "chose up at step {}".format(
                            self.total_steps - self.current_steps - 1
                        )
                    )
                self.path.append(next)

            if self.show:
                print(
                    "new start: x = {} y = {} steps left = {}, new lambda: lam={}".format(
                        self.current_start_x,
                        self.current_start_y,
                        self.current_steps + 1,
                        self.lam,
                    )
                )

            self.current_eps = self.eps

        print(self.path)
        
        if len(next_locs) == 0:
            print("No improvisor found")


def grid_with_path(imp):
    size_x = imp.size_x
    size_y = imp.size_y
    start_x = imp.start_y
    start_y = imp.start_x
    path = imp.path
    grid = [["-" for _ in range(size_x)] for _ in range(size_y)]

    # Starting position
    x, y = start_x, start_y
    step = 0
    # Directions: 'r' -> right, 'd' -> down, 'l' -> left, 'u' -> up
    directions = {"r": (0, 1), "d": (1, 0), "l": (0, -1), "u": (-1, 0)}
    symbols = {"r": "→", "d": "↓", "l": "←", "u": "↑"}

    output = ""

    # Traverse the path and mark the corresponding positions on the grid
    for move in path:
        dx, dy = directions[move]
        grid[x][y] = symbols[move]
        x += dx
        y += dy
        step += 1
        output += f"step {step}\n"
        for row in grid:
            output += " ".join(row) + "\n"
        output += "\n"

    return output
