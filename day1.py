from aocd.models import Puzzle

def num_incrs(nums):
    prev = None
    num_incr = 0
    for curr in nums:
        if prev is not None and curr > prev:
            num_incr += 1
        prev = curr
    return num_incr

print(f"Part 1 Test: {num_incrs([199, 200, 208, 210, 200, 207, 240, 269, 260, 263])}")

def puzzle_input():
    puzzle = Puzzle(year=2021, day=1)
    return [int(line) for line in puzzle.input_data.splitlines()]

print(f"Day 1 Part 1: {num_incrs(puzzle_input())}")

def three_measure_sum(nums, i):
    if i < 2:
        # Error!
        return None
    return nums[i - 2] + nums[i - 1] + nums[i]

#print(three_measure_sum([0, 2, 3, 4, 5, 6], 3))

def num_incrs_three_measure(nums):
    num_incr = 0

    prev_sum = None
    for i in range(2, len(nums)):
        curr_sum = three_measure_sum(nums, i)
        if prev_sum != None and curr_sum > prev_sum:
            num_incr += 1
        prev_sum = curr_sum
    return num_incr

def num_incrs_three_measure2(nums):
    num_incr = 0

    for i in range(0, len(nums) - 3):
        if nums[i + 3] > nums[i]:
            num_incr += 1
    return num_incr

print(f"Part 2 Test: {num_incrs_three_measure2([607, 618, 618, 617, 647, 716, 769, 792])}")

print(f"Day 1 Part 2: {num_incrs_three_measure2(puzzle_input())}")
