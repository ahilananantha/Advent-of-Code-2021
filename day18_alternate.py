from aocd.models import Puzzle
from collections import defaultdict
import copy
import functools

def puzzle_input_data():
    puzzle = Puzzle(year = 2021, day = 18)
    return puzzle.input_data

enable_debug_logging = False
def debug_log(str):
    if enable_debug_logging:
        print(f"debug: {str}")

def snail_add(x, y):
    return [copy.deepcopy(x), copy.deepcopy(y)]

def split_number(x):
    assert isinstance(x, int)
    if x % 2 == 0:
        return [x // 2, x // 2]
    else:
        # rounded down, rounded up
        return [x // 2, (x+1) // 2]

def add_leftmost(x, value):
    if isinstance(x, int):
        return x + value
    return [add_leftmost(x[0], value), x[1]]

def add_rightmost(x, value):
    if isinstance(x, int):
        return x + value
    return [x[0], add_rightmost(x[1], value)]

# returns the reduction of x
def snail_reduce(x):
    # returns (reduced result, if exploded, explosion fragments)
    def explode_helper(x, depth):
        if isinstance(x, int):
            return x, False, None
        if not isinstance(x, list):
           raise Exception(f"snail numbers should only contain lists, but found {type(x).__name__}")
        if len(x) != 2:
            raise Exception(f"snail numbers should only contain lists that are pairs, but found length of {len(x)}")
        if depth == 4:
            # can be exploded, but also ensure the pair components are not lists, since we should never have that much nesting
            if not isinstance(x[0], int) or not isinstance(x[1], int):
                raise Exception(f"found non simple int pair at depth 4: {x}")
            return 0, True, (x[0], x[1])
        # Recursive cases
        (left_result, left_was_exploded, left_fragments) = explode_helper(x[0], depth + 1)
        if left_was_exploded:
            # setting x[0] will be no-op once we bubble up
            x[0] = left_result
            # add right part of the left fragment to right element
            if left_fragments[1] != 0:
                x[1] = add_leftmost(x[1], left_fragments[1])
            # but bubble up left part of the left fragment
            return x, True, (left_fragments[0], 0)
        # Else nothing happened on the left, so try actions on the right
        (right_result, right_was_exploded, right_fragments) = explode_helper(x[1], depth + 1)
        if right_was_exploded:
            # setting x[1] will be no-op once we bubble up
            x[1] = right_result
            # add left part of the right fragment to left element
            if right_fragments[0] != 0:
                x[0] = add_rightmost(x[0], right_fragments[0])
            # but bubble up right part of the left fragment
            return x, True, (0, right_fragments[1])
        # Else nothing to do for either element of this pair
        return x, False, None

    # returns (reduced result, was split)
    def split_helper(x):
        if isinstance(x, int):
            # can it be split?
            if x >= 10:
                return split_number(x), True
            else:
                return x, False
        if not isinstance(x, list):
           raise Exception(f"snail numbers should only contain lists, but found {type(x).__name__}")
        if len(x) != 2:
            raise Exception(f"snail numbers should only contain lists that are pairs, but found length of {len(x)}")
        # Recursive cases
        (left_result, left_was_split) = split_helper(x[0])
        if left_was_split:
            # setting x[0] will be no-op once we bubble up
            x[0] = left_result
            return x, True
        # Else nothing happened on the left, so try actions on the right
        (right_result, right_was_split) = split_helper(x[1])
        if right_was_split:
            # setting x[1] will be no-op once we bubble up
            x[1] = right_result
            return x, True
        # Else nothing to do for either element of this pair
        return x, False
    
    if isinstance(x, int):
        raise Exception("in place reduction invalid for primitives")
    # First check/apply explosions
    (x, was_exploded, _) = explode_helper(x, 0)
    # was modified in place, no need to return
    if was_exploded:
        debug_log(f"after explode: {x}")
        return True

    # Next check/apply splits
    (x, was_split) = split_helper(x)
    if was_split:
        debug_log(f"after split: {x}")
        return True

    return False

def snail_add_and_reduce(x, y):
    summed = snail_add(x, y)
    debug_log(f"after add: {summed}")
    # reduce in place until nothing to do
    did_reduce = True
    while did_reduce:
        did_reduce = snail_reduce(summed)
    return summed

def snail_add_and_reduce_list(snail_nums):
    return functools.reduce(snail_add_and_reduce, snail_nums)

def get_magnitude(x):
    if isinstance(x, int):
        return x
    left_magnitude = get_magnitude(x[0])
    right_magnitude = get_magnitude(x[1])
    return 3*left_magnitude + 2*right_magnitude

def largest_two_sum(snail_numbers):
    # all permutations choosing 2 from the list
    largest = 0
    for i in range(0, len(snail_numbers)):
        for j in range(0, len(snail_numbers)):
            if i != j:
                snail_num = snail_add_and_reduce(snail_numbers[i], snail_numbers[j])
                magnitude = get_magnitude(snail_num)
                largest = max(largest, magnitude)
    return largest

def process_input_data(input):
    lines = input.splitlines()
    snail_number_list = []
    for line in lines:
        snail_number_list.append(eval(line))
    return snail_number_list

explode_test_inputs = [
    [[[[[9,8],1],2],3],4],
    [7,[6,[5,[4,[3,2]]]]],
    [[6,[5,[4,[3,2]]]],1],
    [[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]],
    [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]],
    [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]
]

for input in explode_test_inputs:
    # reduce is in place, so make a copy
    after = copy.deepcopy(input)
    did_reduce = snail_reduce(after)
    assert did_reduce == True
    print(f"Exploding  {input}   ->   {after}")

split_test_inputs = [
    [[[[0,7],4],[15,[0,13]]],[1,1]],
    [[[[0,7],4],[[7,8],[0,13]]],[1,1]]
]

print("")

for input in split_test_inputs:
    # reduce is in place, so make a copy
    after = copy.deepcopy(input)
    did_reduce = snail_reduce(after)
    assert did_reduce == True
    print(f"Splitting  {input}   ->   {after}")

print("")

print(snail_add_and_reduce([[[[4,3],4],4],[7,[[8,4],9]]], [1,1]))

print("")

small_input_list = [
    [1,1],
    [2,2],
    [3,3],
    [4,4],
    [5,5],
    [6,6]
]

print(functools.reduce(snail_add_and_reduce, small_input_list))

print("")

larger_input_list_txt = """\
[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]\
"""

larger_input_list = process_input_data(larger_input_list_txt)

print(functools.reduce(snail_add_and_reduce, larger_input_list))

homework_example_input_list_txt = """\
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]\
"""

homework_example_input_list = process_input_data(homework_example_input_list_txt)

homework_sum = functools.reduce(snail_add_and_reduce, homework_example_input_list)
print(f"Final sum of example input: {homework_sum}")
print(f"Magnitude of final sum for example: {get_magnitude(homework_sum)}")

puzzle_snail_number_list = process_input_data(puzzle_input_data())
puzzle_sum = functools.reduce(snail_add_and_reduce, puzzle_snail_number_list)
print(f"Final sum of puzzle input: {puzzle_sum}")
print(f"Magnitude of final sum: {get_magnitude(puzzle_sum)}")

print(f"Largest 2 sum magnitude for example: {largest_two_sum(homework_example_input_list)}")
print(f"Largest 2 sum magnitude for puzzle: {largest_two_sum(puzzle_snail_number_list)}")
