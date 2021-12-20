from aocd.models import Puzzle
import collections

def day13_input_data():
    puzzle = Puzzle(year = 2021, day = 13)
    return puzzle.input_data

Point = collections.namedtuple("Point", ["x", "y"])

def process_input_data(input_data):
    # first part is a sequence of coordinates (x, y)
    points = []
    lines = input_data.splitlines()
    line_idx = 0
    while line_idx < len(lines):
        if lines[line_idx] == "":
            # skip the line
            line_idx += 1
            break
        (x, y) = map(int, lines[line_idx].split(","))
        points.append(Point(x, y))
        line_idx += 1
    # second part are fold instructions in the format:
    # fold along {x,y}={num}
    fold_instructions = []
    while line_idx < len(lines):
        words = lines[line_idx].split()
        assert words[0] == "fold"
        assert words[1] == "along"
        (axis, pos) = words[2].split("=")
        pos = int(pos)
        fold_instructions.append((axis, pos))
        line_idx += 1
    return (points, fold_instructions)

class Grid:
    def __init__(self, points = []):
        max_x = 0
        max_y = 0
        for point in points:
            max_x = max(max_x, point.x)
            max_y = max(max_y, point.y)
        self.max_x = max_x
        self.max_y = max_y
        self.points = set(points)
    def fold(self, axis, position):
        if axis == "x":
            if position > self.max_x:
                raise Exception("folding off x axis")
            self.max_x = position
        if axis == "y":
            if position > self.max_y:
                raise Exception("folding off y axis")
            self.max_y = position
        new_points = set()
        for point in self.points:
            if axis == "x":
                # folding left
                if point.x == position:
                    raise Exception(f"point detected on fold: {point}")
                elif point.x > position:
                    new_x = position - (point.x - position)
                    if new_x < 0:
                        raise Exception(f"Folded paper too much")
                    new_points.add(Point(x = new_x, y = point.y))
                else:
                    new_points.add(point)
            if axis == "y":
                # folding up
                if point.y == position:
                    raise Exception(f"point detected on fold: {point}")
                elif point.y > position:
                    new_y = position - (point.y - position)
                    if new_y < 0:
                        raise Exception(f"Folded paper too much")
                    new_points.add(Point(x = point.x, y = new_y))
                else:
                    new_points.add(point)
        self.points = new_points
    def num_dots(self):
        return len(self.points)
    def draw(self):
        for y in range(0, self.max_y + 1):
            line = []
            for x in range(0, self.max_x + 1):
                if Point(x, y) in self.points:
                    line.append("#")
                else:
                    line.append(".")
            print("".join(line))


test_input_data = """\
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5\
"""

def apply_first_folding(processed_input):
    (points, fold_instructions) = processed_input
    grid = Grid(points)
    (fold_axis, fold_position) = fold_instructions[0]
    grid.fold(fold_axis, fold_position)
    return grid.num_dots()

#print(process_input_data(test_input_data))

print(apply_first_folding(process_input_data(test_input_data)))
print(apply_first_folding(process_input_data(day13_input_data())))

def apply_folding(processed_input):
    (points, fold_instructions) = processed_input
    grid = Grid(points)
    for (fold_axis, fold_position) in fold_instructions:
        grid.fold(fold_axis, fold_position)
    grid.draw()

apply_folding(process_input_data(test_input_data))
apply_folding(process_input_data(day13_input_data()))
