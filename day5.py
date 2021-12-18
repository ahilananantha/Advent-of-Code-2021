from aocd.models import Puzzle
import collections

debug = False

Point = collections.namedtuple("Point", ["x", "y"])

# VentLine a 2-tuple of points: start and end:
VentLine = collections.namedtuple("VentLine", ["start", "end"])

class FieldCell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.num_vent_lines = 0
        if debug:
            self.vents_line_indices = set()
    def add_vent_line(self, vent_index):
        if debug:
            if vent_index in self.vents_line_indices:
                raise Exception(f"attempt to add same vent line {vent_index} to same field cell")
        self.num_vent_lines += 1
        if debug:
            self.vents_line_indices.add(vent_index)
    def is_dangerous(self):
        return self.num_vent_lines >= 2

class Field:
    def __init__(self, max_x, max_y):
        self.max_x = max_x
        self.max_y = max_y
        self.cells = []
        for y in range(0, max_y + 1):
            row = []
            for x in range(0, max_x + 1):
                row.append(FieldCell(x, y))
            self.cells.append(row)

    def _cell_idx(self, x, y):
        return self.cells[y][x]

    def _point_within_field(self, point):
        return (0 <= point.x <= self.max_x) and (0 <= point.y <= self.max_y)

    def add_vent_line(self, vent_index, vent_line, skip_diagonals = True):
        # make sure points are within the field range we were told
        if not self._point_within_field(vent_line.start):
            raise Exception(f"start point {vent_line.start} is outside of field range ([0:{self.max_x + 1}], [0:{self.max_y + 1}")
        if not self._point_within_field(vent_line.end):
            raise Exception(f"end point {vent_line.end} is outside of field range ([0:{self.max_x + 1}], [0:{self.max_y + 1}]")
        # case 1: vertical line
        if vent_line.start.x == vent_line.end.x:
            for y in range(min(vent_line.start.y, vent_line.end.y), max(vent_line.start.y, vent_line.end.y) + 1):
                #print(f"vent_line:{vent_line} selects ({vent_line.start.x}, {y})")
                self._cell_idx(vent_line.start.x, y).add_vent_line(vent_index)
        # case 2: horizontal line
        elif vent_line.start.y == vent_line.end.y:
            for x in range(min(vent_line.start.x, vent_line.end.x), max(vent_line.start.x, vent_line.end.x) + 1):
                #print(f"vent_line:{vent_line} selects ({x}, {vent_line.start.y})")
                self._cell_idx(x, vent_line.start.y).add_vent_line(vent_index)
        else:
            if skip_diagonals:
                print(f"skipping diagonal vent line: {vent_line}")
                return
            if vent_line.start.x < vent_line.end.x:
                line_start = vent_line.start
                line_end = vent_line.end
            else:
                line_start = vent_line.end
                line_end = vent_line.start
            if line_end.y > line_start.y:
                slope = 1
            else:
                slope = -1
            y = line_start.y
            if debug:
                print("#")
            for x in range(line_start.x, line_end.x + 1):
                self._cell_idx(x, y).add_vent_line(vent_index)
                if debug:
                    print(f"diagonal vent_line:{vent_line} selects ({x},{y})")
                y += slope
            if debug:
                print("#")

    def num_dangerous_points(self):
        num_dangerous = 0
        for y in range(0, self.max_y + 1):
            for x in range(0, self.max_x + 1):
                if self._cell_idx(x, y).is_dangerous():
                    num_dangerous += 1
        return num_dangerous

# vent_lines must be a list of vent_line

def calc_xy_range(vent_lines):
    max_x = 0
    max_y = 0
    for vent_line in vent_lines:
        max_x = max(max_x, vent_line.start.x, vent_line.end.x)
        max_y = max(max_y, vent_line.start.y, vent_line.end.y)
    return (max_x, max_y)

def calc_dangerous_points(vent_lines, skip_diagonals):
    (max_x, max_y) = calc_xy_range(vent_lines)
    field = Field(max_x, max_y)
    for vent_line_idx, vent_line in enumerate(vent_lines):
        field.add_vent_line(vent_line_idx, vent_line, skip_diagonals)
    return field.num_dangerous_points()

def process_input_data(input_data):
    lines = input_data.split("\n")
    vent_lines = []
    for line in lines:
        # Convert:
        #  x1,y1 -> x2,y2
        # Into:
        # VentLine( Point(x1, y1), Point(x2, y2) )
        (coord1, arrow, coord2) = line.split()
        (start_x, start_y) = map(int, coord1.split(","))
        (end_x, end_y) = map(int, coord2.split(","))
        vent_lines.append( VentLine( Point(x = start_x, y = start_y), Point(x = end_x, y = end_y) ) )
    return vent_lines

def day5_input_data():
    puzzle = Puzzle(year = 2021, day = 5)
    return puzzle.input_data

test_input_data="""\
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2\
"""

test_vent_lines = process_input_data(test_input_data)
#print(calc_xy_range(test_vent_lines))
print(f"Test value (no diagonals): {calc_dangerous_points(test_vent_lines, skip_diagonals=True)}")

day5_vent_lines = process_input_data(day5_input_data())
#print(calc_xy_range(day5_vent_lines))
print(f"Day5 data value (no diagonals): {calc_dangerous_points(day5_vent_lines, skip_diagonals=True)}")

print(f"Test value (with diagonals): {calc_dangerous_points(test_vent_lines, skip_diagonals=False)}")
print(f"Day5 data value (with diagonals): {calc_dangerous_points(day5_vent_lines, skip_diagonals=False)}")
