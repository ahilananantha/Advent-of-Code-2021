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

def split_number(num):
    if num % 2 == 0:
        return num // 2, num // 2
    else:
        # round down, round up
        return num // 2, (num+1) // 2

class SnailNode:
    def __init__(self, num=None, left=None, right=None):
        if num == None:
            assert left != None and right != None
        if num != None:
            assert left == None and right == None
        self.num = num
        self.left = left
        self.right = right
    def assert_is_regular_num(self):
        assert self.num != None
        assert self.left == None
        assert self.right == None
    def assert_is_pair(self):
        assert self.num == None
        assert self.left != None
        assert self.right != None
    def is_regular_num(self):
        return self.num != None
    def is_pair(self):
        return self.left != None and self.right != None
    def should_split(self):
        self.assert_is_regular_num()
        return self.num >= 10
    def split(self):
        self.assert_is_regular_num()
        assert self.num >= 10
        left_val, right_val = split_number(self.num)
        self.left = SnailNode(left_val)
        self.right = SnailNode(right_val)
        self.num = None
    def absorb(self, fragment):
        self.assert_is_regular_num()
        self.num += fragment
    def explode(self):
        self.assert_is_pair()
        assert self.left.is_regular_num()
        assert self.right.is_regular_num()
        left_num = self.left.num
        right_num = self.right.num
        # convert to regular number with value 0
        self.num = 0
        self.left = None
        self.right = None
        # and explode out the values
        return left_num, right_num
    def to_snail_number(self):
        if self.is_regular_num():
            return self.num
        else:
            return [self.left.to_snail_number(), self.right.to_snail_number()]

def build_snail_tree(snail_number):
    if isinstance(snail_number, int):
        return SnailNode(num=snail_number)
    return SnailNode(left=build_snail_tree(snail_number[0]),
                       right=build_snail_tree(snail_number[1]))

def add_snail_trees(snail_x, snail_y):
    return SnailNode(left=snail_x, right=snail_y)

def inorder_snail_tree(root):
    res = []
    def dfs_helper(node):
        if node.left is not None:
            dfs_helper(node.left)
        res.append(node)
        if node.right is not None:
            dfs_helper(node.right)
    dfs_helper(root)
    return res

def reduce_snail_tree(root):
    inorder_list = inorder_snail_tree(root)
    def get_pred_num_node(curr):
        prev_num_node = None
        for node in inorder_list:
            if node == curr:
                return prev_num_node
            if node.is_regular_num():
                prev_num_node = node
        assert False
    def get_succ_num_node(curr):
        i = 0
        while i < len(inorder_list):
            if inorder_list[i] == curr:
                i += 1
                break
            i += 1
        while i < len(inorder_list):
            if inorder_list[i].is_regular_num():
                return inorder_list[i]
            i += 1
        return None

    def split_helper(node):
        if node.is_regular_num():
            if node.should_split():
                node.split()
                # Split
                return True
            return False
        # Recurse left
        if split_helper(node.left):
            return True
        # Only continue to right if there was no reduction already done
        if split_helper(node.right):
            return True
        # No reduction done/needed
        return False

    # returns True if the tree was reduced
    def explode_helper(node, depth):
        if node.is_regular_num():
            return False
        if depth == 4:
            left_num_node = node.left
            right_num_node = node.right
            (left_frag, right_frag) = node.explode()
            pred = get_pred_num_node(left_num_node)
            if pred is not None:
                pred.absorb(left_frag)
            succ = get_succ_num_node(right_num_node)
            if succ is not None:
                succ.absorb(right_frag)
            # Explosion
            return True
        # Recurse left
        if explode_helper(node.left, depth + 1):
            return True
        # Only continue to right if there was no reduction already done
        if explode_helper(node.right, depth + 1):
            return True
        # No reduction done/needed
        return False
    
    did_explode = explode_helper(root, 0)
    if did_explode:
        debug_log(f"Exploding to: {root.to_snail_number()}")
        return True
    did_split = split_helper(root)
    if did_split:
        debug_log(f"Splitting to: {root.to_snail_number()}")
        return True
    return False

def snail_add_and_reduce_trees(snail_tree_x, snail_tree_y):
    tree_sum = add_snail_trees(snail_tree_x, snail_tree_y)
    did_reduce = True
    while did_reduce:
        did_reduce = reduce_snail_tree(tree_sum)
    return tree_sum

def snail_add_and_reduce(snail_numbers):
    if len(snail_numbers) < 2:
        return snail_numbers
    tree_sum = build_snail_tree(snail_numbers[0])
    for i in range(1, len(snail_numbers)):
        tree_operand = build_snail_tree(snail_numbers[i])
        tree_sum = snail_add_and_reduce_trees(tree_sum, tree_operand)
        debug_log(f"Partial sum: {tree_sum.to_snail_number()}")
    return tree_sum.to_snail_number()

def get_magnitude(snail_number):
    if isinstance(snail_number, int):
        return snail_number
    left_magnitude = get_magnitude(snail_number[0])
    right_magnitude = get_magnitude(snail_number[1])
    return 3*left_magnitude + 2*right_magnitude

def largest_two_sum(snail_numbers):
    # all permutations choosing 2 from the list
    largest = 0
    for i in range(0, len(snail_numbers)):
        for j in range(0, len(snail_numbers)):
            if i != j:
                snail_num = snail_add_and_reduce([snail_numbers[i], snail_numbers[j]])
                magnitude = get_magnitude(snail_num)
                largest = max(largest, magnitude)
    return largest

def process_input_data(input):
    lines = input.splitlines()
    snail_number_list = []
    for line in lines:
        snail_number_list.append(eval(line))
    return snail_number_list

snail_nums_str = """\
[1,2]
[[1,2],3]
[9,[8,7]]
[[1,9],[8,5]]
[[[[1,2],[3,4]],[[5,6],[7,8]]],9]
[[[9,[3,8]],[[0,9],6]],[[[3,7],[4,9]],3]]
[[[[1,3],[5,3]],[[1,3],[8,7]]],[[[4,9],[6,9]],[[8,2],[7,3]]]]\
"""

snail_nums = process_input_data(snail_nums_str)

for snail_num in snail_nums:
    snail_tree = build_snail_tree(snail_num)
    assert snail_tree.to_snail_number() == snail_num
    node_list = inorder_snail_tree(snail_tree)
    nums = []
    for node in node_list:
        if node.is_regular_num():
            nums.append(node.num)
    print(nums)

explode_test_inputs = [
    [[[[[9,8],1],2],3],4],
    [7,[6,[5,[4,[3,2]]]]],
    [[6,[5,[4,[3,2]]]],1],
    [[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]],
    [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]],
    [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]
]

for input in explode_test_inputs:
    root = build_snail_tree(input)
    did_reduce = reduce_snail_tree(root)
    assert did_reduce == True
    after = root.to_snail_number()
    print(f"Exploding  {input}   ->   {after}")

split_test_inputs = [
    [[[[0,7],4],[15,[0,13]]],[1,1]],
    [[[[0,7],4],[[7,8],[0,13]]],[1,1]]
]

print("")

for input in split_test_inputs:
    root = build_snail_tree(input)
    did_reduce = reduce_snail_tree(root)
    assert did_reduce == True
    after = root.to_snail_number()
    print(f"Splitting  {input}   ->   {after}")

print("")

print(snail_add_and_reduce([ [[[[4,3],4],4],[7,[[8,4],9]]], [1,1] ]))

print("")

small_input_list = [
    [1,1],
    [2,2],
    [3,3],
    [4,4],
    [5,5],
    [6,6]
]

print(snail_add_and_reduce(small_input_list))

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

print(snail_add_and_reduce(larger_input_list))

print(get_magnitude([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]))

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

homework_sum = snail_add_and_reduce(homework_example_input_list)
print(f"Final sum of example input: {homework_sum}")
print(f"Magnitude of final sum for example: {get_magnitude(homework_sum)}")

puzzle_snail_number_list = process_input_data(puzzle_input_data())
#print(puzzle_snail_number_list)
puzzle_sum = snail_add_and_reduce(puzzle_snail_number_list)
print(f"Final sum of puzzle input: {puzzle_sum}")
print(f"Magnitude of final sum: {get_magnitude(puzzle_sum)}")

print(f"Largest 2 sum magnitude for example: {largest_two_sum(homework_example_input_list)}")
print(f"Largest 2 sum magnitude for puzzle: {largest_two_sum(puzzle_snail_number_list)}")