from aocd.models import Puzzle

def num_incrs(nums):
    prev = None
    num_incr = 0
    for curr in nums:
        if prev != None and curr > prev:
            num_incr += 1
        prev = curr
    return num_incr

#print(num_incrs([199, 200, 208, 210, 200, 207, 240, 269, 260, 263]))

def day1_part1():
    puzzle = Puzzle(year=2021, day=1)
    nums = [int(line) for line in puzzle.input_data.split('\n')]
    return num_incrs(nums)

#print(f"Day 1 Part 1{day1_part1()}")

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

#print(num_incrs_three_measure([607, 618, 618, 617, 647, 716, 769, 792]))

def day1_part2():
    puzzle = Puzzle(year = 2021, day = 1)
    nums = [int(line) for line in puzzle.input_data.split('\n')]
    return num_incrs_three_measure(nums)

#print(f"Day1 Part2: {day1_part2()}")
