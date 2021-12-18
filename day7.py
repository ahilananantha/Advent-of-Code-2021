from aocd.models import Puzzle

def process_input_data(input_data):
    lines = input_data.split("\n")
    if len(lines) > 1:
        raise Exception(f"expected only 1 line of input, but got {len(lines)}")
    nums = [int(x) for x in lines[0].split(",")]
    return nums

def day7_input_data():
    puzzle = Puzzle(year = 2021, day = 7)
    return puzzle.input_data

test_input_data = """\
16,1,2,0,4,2,7,1,2,14\
"""

test_input_nums = process_input_data(test_input_data)
print(f"Test input: {test_input_nums}")

def median(vals):
    s = sorted(vals)
    mid = len(vals) // 2
    if len(vals) % 2 == 1:
        return s[mid]
    else:
        return (s[mid - 1] + s[mid]) // 2

def mean(vals):
    return sum(vals) / len(vals)

def part1_fuel_cost(start_pos, end_pos):
    distance = abs(end_pos - start_pos)
    return distance

def how_much_fuel(positions, end_pos, fuel_cost_func):
    return sum([fuel_cost_func(start_pos, end_pos) for start_pos in positions])

def part1_how_much_fuel(positions, end_pos):
    return how_much_fuel(positions, end_pos, part1_fuel_cost)

def part1_optimal(positions):
    end_pos = median(positions)
    return part1_how_much_fuel(positions, end_pos)

print(f"median of test input positions = {median(test_input_nums)}")
print(f"test input, how much fuel (part1): {part1_optimal(test_input_nums)}")

day7_nums = process_input_data(day7_input_data())

print(f"real input, how much fuel (part1) {part1_optimal(day7_nums)}")

def part2_fuel_cost(start_pos, end_pos):
    distance = abs(end_pos - start_pos)
    # fuel cost is the summation from 1 to distance
    return distance * (distance + 1) // 2

def part2_how_much_fuel(positions, end_pos):
    return how_much_fuel(positions, end_pos, part2_fuel_cost)

def part2_optimal(positions):
    end_pos_from_mean = int(mean(positions))
    fuel_cost = part2_how_much_fuel(positions, end_pos_from_mean)
    lowest_fuel_cost = fuel_cost
    if end_pos_from_mean > 0:
        fuel_cost = part2_how_much_fuel(positions, end_pos_from_mean - 1)
        if fuel_cost < lowest_fuel_cost:
            lowest_fuel_cost = fuel_cost
    fuel_cost = part2_how_much_fuel(positions, end_pos_from_mean + 1)
    if fuel_cost < lowest_fuel_cost:
        lowest_fuel_cost = fuel_cost
    return lowest_fuel_cost

print(f"mean of test input is {mean(test_input_nums)}")
print(f"test input, how much fuel (part2): {part2_optimal(test_input_nums)}")
print(f"real input, how much fuel (part2) {part2_optimal(day7_nums)}")

