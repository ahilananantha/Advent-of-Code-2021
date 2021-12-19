from aocd.models import Puzzle
from collections import deque

test_input_data = """\
2199943210
3987894921
9856789892
8767896789
9899965678\
"""

def day9_input_data():
    puzzle = Puzzle(year = 2021, day = 9)
    return puzzle.input_data

def process_input_data(input_data):
    lines = input_data.splitlines()
    # Each line is a stream of digits of equal length
    heights = []
    for line in lines:
        row = []
        for c in line:
            row.append(int(c))
        heights.append(row)
    return heights

#print(test_input_data)
#print(process_input_data(test_input_data))

def find_low_points(heights):
    low_points = []
    nrows = len(heights)
    ncols = len(heights[0])
    for i in range(0, nrows):
        for j in range(0, ncols):
            # is it a low point?
            #surrounding_points = ""
            if i > 0:
                # up height
                if heights[i - 1][j] <= heights[i][j]:
                    continue
                #surrounding_points += f"up_height: {heights[i-1][j]}, "
            if i < nrows - 1:
                # down height
                if heights[i + 1][j] <= heights[i][j]:
                    continue
                #surrounding_points += f"down_height: {heights[i + 1][j]}, "
            if j < ncols - 1:
                # right height
                if heights[i][j + 1] <= heights[i][j]:
                    continue
                #surrounding_points += f"right_height: {heights[i][j + 1]}, "
            if j > 0:
                # left height
                if heights[i][j - 1] <= heights[i][j]:
                    continue
                #surrounding_points += f"left_height: {heights[i][j - 1]}, "
            #print(f"heights[{i}][{j}] = {heights[i][j]}, {surrounding_points}")
            low_points.append((i, j))
    return low_points

test_heights = process_input_data(test_input_data)
print(f"Test input low points: {find_low_points(test_heights)}")

def find_risk_level(heights):
    total_risk_level = 0
    low_points = find_low_points(heights)
    for (row, col) in low_points:
        # risk level is one plus the height
        risk_level = heights[row][col] + 1
        total_risk_level += risk_level
    return total_risk_level

print(f"Test input risk level: {find_risk_level(test_heights)}")

day9_heights = process_input_data(day9_input_data())

#day9_low_points = find_low_points(day9_heights)
#print(f"Day 9 input low points: {day9_low_points}")

print(f"Day 9 input risk level: {find_risk_level(day9_heights)}")

# Directed graph problem where low points are the source points of
# the graphs in a forest

def find_basin_neighbors(heights, vertex):
    def get_height(v):
        return heights[v[0]][v[1]]

    # a basin neighbor is defined as a vertex that's either one up,
    # down, left, or right from the vertex that is of higher height.
    # except for a height of 9, which is excluded from all basins.
    neighbors = []
    num_rows = len(heights)
    num_cols = len(heights[0])
    vertex_height = get_height(vertex)
    if vertex[0] > 0:
        # up vertex
        up_vertex = (vertex[0] - 1, vertex[1])
        up_h = get_height(up_vertex)
        if up_h != 9 and up_h > vertex_height:
            neighbors.append(up_vertex)
    if vertex[0] < num_rows - 1:
        # down vertex
        down_vertex = (vertex[0] + 1, vertex[1])
        down_h = get_height(down_vertex)
        if down_h != 9 and down_h > vertex_height:
            neighbors.append(down_vertex)
    if vertex[1] > 0:
        # left vertex
        left_vertex = (vertex[0], vertex[1] - 1)
        left_h = get_height(left_vertex)
        if left_h != 9 and left_h > vertex_height:
            neighbors.append(left_vertex)
    if vertex[1] < num_cols - 1:
        # right vertex
        right_vertex = (vertex[0], vertex[1] + 1)
        right_h = get_height(right_vertex)
        if right_h != 9 and right_h > vertex_height:
            neighbors.append(right_vertex)
    return neighbors

def basin_bfs(visited, heights, low_point):
    # While marking vertices visited we need to also calculate the size of
    # the connected component and return it
    if low_point in visited:
        raise Exception(f"low point {low_point} should not already be visited")
    q = deque([low_point])
    visited.add(low_point)
    basin_size = 1
    while len(q) > 0:
        node = q.popleft()
        neighbors = find_basin_neighbors(heights, node)
        for neighbor in neighbors:
            if neighbor not in visited:
                q.append(neighbor)
                visited.add(neighbor)
                basin_size += 1
    return basin_size

def find_basins(heights):
    low_points = find_low_points(heights)
    if len(low_points) < 3:
        raise Exception("not enough basins to calculate product")
    num_basins = len(low_points)
    # mark all the low points visited so they will be treated as separate graph
    # connected components.
    visited = set()
    # now run bfs from each low point
    basin_sizes = []
    for low_point in low_points:
        basin_size = basin_bfs(visited, heights, low_point)
        basin_sizes.append(basin_size)
    basin_sizes.sort()
    return basin_sizes[num_basins - 3] * basin_sizes[num_basins - 2] * basin_sizes[num_basins - 1]

print(f"Test input basin product: {find_basins(test_heights)}")

print(f"Day 9 basin product: {find_basins(day9_heights)}")
