from aocd.models import Puzzle

test1_input =  [
    "00100",
    "11110",
    "10110",
    "10111",
    "10101",
    "01111",
    "00111",
    "11100",
    "10000",
    "11001",
    "00010",
    "01010"
]

def find_most_common_bits(input):
    num_bits = len(input[0])
    total_nums = len(input)
    ones_freqs = [0] * num_bits
    for bit_str in input:
        for bit_num, bit_val in enumerate(bit_str):
            if bit_val == "1":
                ones_freqs[bit_num] += 1
    most_common = []
    for bit_num, ones_freq in enumerate(ones_freqs):
        if ones_freq >= (total_nums - ones_freq):
            # most common bit val is one at pos bit_num
            # or equally common
            most_common.append(1)
        else:
            # most common bit val is zero at pos bit_num
            most_common.append(0)
    return most_common

def power_consumption(input):
    num_bits = len(input[0])
    most_common = find_most_common_bits(input)
    gamma_rate = 0
    epsilon_rate = 0
    for bit_num, most_common in enumerate(most_common):
        if most_common == 1:
            # most common bit val is one at pos bit_num 
            gamma_rate |= 1 << (num_bits - bit_num - 1)
        else: # most_common == 0:
            # most common bit val is zero at pos bit_num
            epsilon_rate |= 1 << (num_bits - bit_num - 1)
    return gamma_rate * epsilon_rate

def day3_part1_test1():
    return power_consumption(test1_input)

print(f"Day3 Part1 Test1: {day3_part1_test1()}")

def day3_part1():
    puzzle = Puzzle(year = 2021, day = 3)
    input = puzzle.input_data.split("\n")
    return power_consumption(input)

print(f"Day3 Part1: {day3_part1()}")

def find_most_common_bit(input, bit_num):
    ones_freq = 0
    for bit_str in input:
        if bit_str[bit_num] == "1":
            ones_freq += 1
    if ones_freq >= (len(input) - ones_freq):
        return 1
    else:
        return 0

def bit_filter_helper(input, use_most_common):
    in_list = input[:]
    num_bits = len(in_list[0])
    for bit_num in range(0, num_bits):
        if len(in_list) == 1:
            break
        most_common_bit_val = find_most_common_bit(in_list, bit_num)
        out_list = []
        if use_most_common:
            match_bit = most_common_bit_val
        else:
            match_bit = most_common_bit_val ^ 1
        for bit_str in in_list:
            if int(bit_str[bit_num]) == match_bit:
                # Keep
                out_list.append(bit_str)
        in_list = out_list
    return in_list[0]

def life_support_rating(input):
    num_bits = len(input[0])

    oxygen_generator_match = bit_filter_helper(input, True)
    #print(f"oxygen_generator_match = {oxygen_generator_match}")
    co2_scrubber_match = bit_filter_helper(input, False)
    #print(f"co2_scrubber_match = {co2_scrubber_match}")

    # Convert to numbers
    oxygen_generator_rating = 0
    for bit_num, bit_val in enumerate(oxygen_generator_match):
        if bit_val == '1':
            oxygen_generator_rating |= 1 << (num_bits - bit_num - 1)
    #print(f"oxygen_generator_rating = {oxygen_generator_rating}")
    co2_scrubber_rating = 0
    for bit_num, bit_val in enumerate(co2_scrubber_match):
        if bit_val == '1':
            co2_scrubber_rating |= 1 << (num_bits - bit_num - 1)
    #print(f"co2_scrubber_rating = {co2_scrubber_rating}")

    return oxygen_generator_rating * co2_scrubber_rating

def day3_part2_test1():
    return life_support_rating(test1_input)

print(f"Day3 Part2 Test1: {day3_part2_test1()}")

def day3_part2():
    puzzle = Puzzle(year = 2021, day = 3)
    input = puzzle.input_data.split("\n")
    return life_support_rating(input)

print(f"Day3 Part2: {day3_part2()}")
