from aocd.models import Puzzle
from collections import deque
import heapq

def puzzle_input_data():
    puzzle = Puzzle(year = 2021, day = 15)
    return puzzle.input_data

test_input_data = """\
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581\
"""

def process_input_data(input_data):
    lines = input_data.splitlines()
    risk_level_matrix = []
    for line in lines:
        row = []
        for c in line:
            row.append(int(c))
        risk_level_matrix.append(row)
    return risk_level_matrix

#print(process_input_data(test_input_data))

class HeapNode:
    def __init__(self, total_risk, coord, parent_coord):
        self.total_risk = total_risk
        self.coord = coord
        self.parent_coord = parent_coord
    def __lt__(self, other):
        return self.total_risk < other.total_risk

def lowest_risk_path(risk_level_matrix, dim_multiplier = 1):
    matrix_nrows = len(risk_level_matrix)
    nrows = matrix_nrows * dim_multiplier

    matrix_ncols = matrix_nrows
    ncols = matrix_ncols * dim_multiplier

    visited = set()
    # total risk is the total risk for the shortest path
    # from the start to that node. indexed by coordinate
    # value is a pair of total risk value and the parent
    # coordinate in the path to it.
    total_risk = {}
    
    def is_valid_coord(coord):
        return 0 <= coord[0] < nrows and 0 <= coord[1] < ncols 

    def get_tile_coord(coord):
        tile_row = coord[0] // matrix_nrows
        tile_col = coord[1] // matrix_ncols
        return (tile_row, tile_col)

    def lookup_risk_level(coord):
        tile_value = risk_level_matrix[coord[0] % matrix_nrows][coord[1] % matrix_ncols]
        tile_coord = get_tile_coord(coord)
        value = tile_value + tile_coord[0] + tile_coord[1]
        while value > 9:
            value -= 9
        return value

    def get_neighbors(coord):
        neighbors = []
        for move in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            adjacent_coord = (coord[0] + move[0], coord[1] + move[1])
            if is_valid_coord(adjacent_coord):
                neighbors.append(adjacent_coord)
        return neighbors

    def calc_shortest_path():
        # Start with top left node as we already know the shortest path to it is 0
        heap = []
        start_node = HeapNode(0, (0, 0), None)
        heapq.heappush(heap, start_node)
        while len(heap) > 0:
            curr_node = heapq.heappop(heap)
            if curr_node.coord in visited:
                # we already picked a better path
                continue
            visited.add(curr_node.coord)
            total_risk[curr_node.coord] = (curr_node.total_risk, curr_node.parent_coord)
            if curr_node.coord == (nrows - 1, ncols - 1):
                # got to the final position
                break
            for neighbor_coord in get_neighbors(curr_node.coord):
                if neighbor_coord not in visited:
                    neighbor_total_risk = curr_node.total_risk + lookup_risk_level(neighbor_coord)
                    neighbor_node = HeapNode(neighbor_total_risk, neighbor_coord, curr_node.coord)
                    heapq.heappush(heap, neighbor_node)

    def get_path():
        path = []
        coord = (nrows - 1, ncols - 1)
        while coord != None:
            path.append(coord)
            coord = total_risk[coord][1]
        path.reverse()
        return path

    calc_shortest_path()
    return (total_risk[(nrows - 1, ncols - 1)][0], get_path())

def draw_path(path):
    matrix = []
    nrows = path[-1][0] + 1
    ncols = path[-1][1] + 1
    for i in range(0, nrows):
        matrix.append([" "] * ncols)
    for coord in path:
        matrix[coord[0]][coord[1]] = "#"
    for i in range(0, nrows):
        print("".join(matrix[i]))

def detect_up_or_left_move(path):
    for i in range(0, len(path) - 1):
        if path[i + 1][0] < path[i][0]:
            print(f"   up move from: {path[i]} to {path[i+1]}")
        if path[i + 1][1] < path[i + 1][1]:
            print(f"   left move from: {path[i]} to {path[i+1]}")

(test_lowest_risk, test_path) = lowest_risk_path(process_input_data(test_input_data))
print(f"Test input lowest total risk path: {test_lowest_risk}")
#draw_path(test_path)
detect_up_or_left_move(test_path)

(puzzle_lowest_risk, puzzle_path) = lowest_risk_path(process_input_data(puzzle_input_data()))
print(f"Puzzle input lowest total risk path: {puzzle_lowest_risk}")
#draw_path(puzzle_path)
detect_up_or_left_move(puzzle_path)

(test_lowest_risk_5x, test_path_5x) = lowest_risk_path(process_input_data(test_input_data), dim_multiplier=5)
print(f"Test input (5x) lowest total risk path: {test_lowest_risk_5x}")
#draw_path(test_path_5x)
detect_up_or_left_move(test_path_5x)

(puzzle_lowest_risk_5x, puzzle_path_5x) = lowest_risk_path(process_input_data(puzzle_input_data()), dim_multiplier=5)
print(f"Puzzle input (5x) lowest total risk path: {puzzle_lowest_risk_5x}")
#draw_path(puzzle_path_5x)
detect_up_or_left_move(puzzle_path_5x)
