from logging import root
from aocd.models import Puzzle
import copy

test_input_data = """\
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526\
"""

def day11_input_data():
    puzzle = Puzzle(year = 2021, day = 11)
    return puzzle.input_data

def process_input_data(input_data):
    lines = input_data.splitlines()
    energies = []
    for line in lines:
        row = []
        for c in line:
            row.append(int(c))
        energies.append(row)
    return energies

#print(process_input_data(test_input_data))

def increment_energies(energies):
    flashing_vertices = []
    num_rows = len(energies)
    num_cols = len(energies[0])

    # increment anything not already flashing (value of 10)
    for i in range(0, num_rows):
        for j in range(0, num_cols):
            if energies[i][j] < 10:
                energies[i][j] += 1
                if energies[i][j] == 10:
                    flashing_vertices.append((i, j))

    return flashing_vertices

def get_adjacent(v, num_rows, num_cols):
    # include diagonally adjacent this time
    adjacent = []
    if v[0] > 0:
        # up vertex
        adjacent.append((v[0] - 1, v[1]))
        if v[1] > 0:
            # up left
            adjacent.append((v[0] - 1, v[1] - 1))
        if v[1] < num_cols - 1:
            # up right
            adjacent.append((v[0] - 1, v[1] + 1))
    if v[0] < num_rows - 1:
        # down vertex
        adjacent.append((v[0] + 1, v[1]))
        if v[1] > 0:
            # down left
            adjacent.append((v[0] + 1, v[1] - 1))
        if v[1] < num_cols - 1:
            # down right
            adjacent.append((v[0] + 1, v[1] + 1))
    if v[1] > 0:
        # left vertex
        adjacent.append((v[0], v[1] - 1))
    if v[1] < num_cols - 1:
        # right vertex
        adjacent.append((v[0], v[1] + 1))
    return adjacent

def increment_adjacent(energies, flashing_vertices):
    new_flashing = []
    num_rows = len(energies)
    num_cols = len(energies[0])

    # increment adjacent octupuses of the ones that are maxed out, if they are
    # not already maxed out
    for vertex in flashing_vertices:
        for adjacent in get_adjacent(vertex, num_rows, num_cols):
            if energies[adjacent[0]][adjacent[1]] < 10:
                energies[adjacent[0]][adjacent[1]] += 1
                # if that makes them start flashing, record that
                if energies[adjacent[0]][adjacent[1]] == 10:
                    new_flashing.append(adjacent)
    # return the list of newly flashing vertices, since we need to loop until
    # there are no more newly flashing vertices
    return new_flashing

def zero_out_flashing(energies):
    num_rows = len(energies)
    num_cols = len(energies[0])

    # 0 out the flashing ones (value of 10)
    total_flashing = 0
    for i in range(0, num_rows):
        for j in range(0, num_cols):
            if energies[i][j] == 10:
                energies[i][j] = 0
                total_flashing += 1
    return total_flashing

# warning: this modifies the energies in place
def one_step(energies):
    num_flashing = 0
    flashing_vertices = increment_energies(energies)
    num_flashing += len(flashing_vertices)

    while len(flashing_vertices) > 0:
        flashing_vertices = increment_adjacent(energies, flashing_vertices)
        num_flashing += len(flashing_vertices)

    total_flashing = zero_out_flashing(energies)
    assert num_flashing == total_flashing
    return num_flashing

def calc_total_flashes(energies, num_steps):
    # make a full copy of the energies
    energies = copy.deepcopy(energies)

    total_flashes = 0
    for i in range(0, num_steps):
        total_flashes += one_step(energies)
    return total_flashes

test_energies = process_input_data(test_input_data)
day11_energies = process_input_data(day11_input_data())

print(f"Test input, num flashes after 10 steps: {calc_total_flashes(test_energies, 10)}")
print(f"Test input, num flashes after 100 steps: {calc_total_flashes(test_energies, 100)}")

print(f"Day 11 input, num flashes after 10 steps: {calc_total_flashes(day11_energies, 10)}")
print(f"Day 11 input, num flashes after 100 steps: {calc_total_flashes(day11_energies, 100)}")

def find_all_flashing(energies):
    # make a full copy of the energies
    energies = copy.deepcopy(energies)
    total_size = len(energies) * len(energies[0])

    num_steps = 1
    while num_steps <= 1000:
        flashes = one_step(energies)
        if flashes == total_size:
            return num_steps
        num_steps += 1
    raise Exception("number of steps exceeded limit")

print(f"Test input, all octopuses flash after {find_all_flashing(test_energies)} steps")
print(f"Test input, all octopuses flash after {find_all_flashing(day11_energies)} steps")