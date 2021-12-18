from aocd.models import Puzzle

def one_day(nums):
    orig_len = len(nums)
    for i in range(0, orig_len):
        if nums[i] == 0:
            nums[i] = 6
            nums.append(8)
        else:
            nums[i] -= 1

def n_days(nums, n):
    for i in range(0, n):
        one_day(nums)

def num_fish_after_slow(nums, days):
    after = nums[:]
    n_days(after, days)
    return len(after)

def num_fish_after(nums, num_days):
    adults_breeding_today = [0] * 7
    newborns_breeding_today = [0] * 9
    for num in nums:
        adults_breeding_today[num] += 1
    assert sum(adults_breeding_today) == len(nums)
    for day_no in range(0, num_days):
        num_adult_breeders_today = adults_breeding_today[day_no % 7]
        num_newborn_breeders_today = newborns_breeding_today[day_no % 9]
        # for each adult breeding today, contribute a newborn breeding 9 days from now, note
        # that's the same index we're operating on, so we had to save the previous value!
        newborns_breeding_today[day_no % 9] += num_adult_breeders_today
        # for each newborn breeding today, contribute a newborn breeding 9 days from now also
        newborns_breeding_today[day_no % 9] += num_newborn_breeders_today
        # but each those newborns breeding today is now an adult, so note that it can instead
        # breed again 7 days from now
        newborns_breeding_today[day_no % 9] -= num_newborn_breeders_today
        adults_breeding_today[day_no % 7] += num_newborn_breeders_today
    return sum(adults_breeding_today) + sum(newborns_breeding_today)

def process_input_data(input_data):
    lines = input_data.split("\n")
    if len(lines) > 1:
        raise Exception(f"expected only 1 line of input, but got {len(lines)}")
    nums = [int(x) for x in lines[0].split(",")]
    return nums

def day6_input_data():
    puzzle = Puzzle(year = 2021, day = 6)
    return puzzle.input_data

test_input_data = """\
3,4,3,1,2\
"""

test_input_nums = process_input_data(test_input_data)
#print(test_input_nums)

print(f"Slow: Test input, num fish after 18 days: {num_fish_after_slow(test_input_nums, 18)}")
print(f"Fast: Test input, num fish after 18 days: {num_fish_after(test_input_nums, 18)}")

puzzle_input_nums = process_input_data(day6_input_data())
#print(puzzle_input_nums)

print(f"Slow: Puzzle input, num fish after 80 days: {num_fish_after_slow(puzzle_input_nums, 80)}")
print(f"Fast: Puzzle input, num fish after 80 days: {num_fish_after(puzzle_input_nums, 80)}")

print(f"Test input, num fish after 256 days: {num_fish_after(test_input_nums, 256)}")
print(f"Puzzle input, num fish after 256 days: {num_fish_after(puzzle_input_nums, 256)}")


