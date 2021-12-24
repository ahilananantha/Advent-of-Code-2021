from aocd.models import Puzzle
from collections import defaultdict
import copy
import functools

enable_debug_logging = True
def debug_log(str):
    if enable_debug_logging:
        print(f"debug: {str}")

def puzzle_input_data():
    puzzle = Puzzle(year = 2021, day = 18)
    return puzzle.input_data

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

larger_input_list = [
    [[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]],
    [7,[[[3,7],[4,3]],[[6,3],[8,8]]]],
    #[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]],
    #[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]],
    #[7,[5,[[3,8],[1,4]]]],
    #[[2,[2,2]],[8,[8,1]]],
    #[2,9],
    #[1,[[[9,3],9],[[9,0],[0,7]]]],
    #[[[5,[7,4]],7],1],
    #[[[[4,2],2],6],[8,7]]
]

print(functools.reduce(snail_add_and_reduce, larger_input_list))
