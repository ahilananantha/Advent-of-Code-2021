from aocd.models import Puzzle

class PositionPart1:
    def __init__(self, horizontal, depth):
        self.horizontal = horizontal
        self.depth = depth
    def down(self, val):
        self.depth += val
    def up(self, val):
        self.depth -= val
    def forward(self, val):
        self.horizontal += val
    def product(self):
        return self.horizontal * self.depth
    def __str__(self):
        return f"Horizontal: {self.horizontal}, Depth: {self.depth}"

class PositionPart2:
    def __init__(self, horizontal, depth, aim = 0):
        self.horizontal = horizontal
        self.depth = depth
        self.aim = aim
    def down(self, val):
        self.aim += val
    def up(self, val):
        self.aim -= val
    def forward(self, val):
        self.horizontal += val
        self.depth += self.aim * val
    def product(self):
        return self.horizontal * self.depth
    def __str__(self):
        return f"Horizontal: {self.horizontal}, Depth: {self.depth}"

def apply_cmd(pos, cmd):
    words = cmd.split(" ")
    (operation, value) = (words[0], int(words[1]))
    if operation == "forward":
        pos.forward(value)
    elif operation == "down":
        pos.down(value)
    elif operation == "up":
        pos.up(value)

def apply_cmds(pos, cmds):
    for cmd in cmds:
        apply_cmd(pos, cmd)
    return pos

def day2_part1_test1():
    cmds = ["forward 5", "down 5", "forward 8", "up 3", "down 8", "forward 2"]
    pos = PositionPart1(0, 0)
    apply_cmds(pos, cmds)
    return pos

print(f"Day2 Part1 Test1: {day2_part1_test1()}")

def day2_part1():
    puzzle = Puzzle(year = 2021, day = 2)
    cmds = puzzle.input_data.split("\n")
    pos = PositionPart1(0, 0)
    apply_cmds(pos, cmds)
    return pos.product()

print(f"Day2 Part1: {day2_part1()}")

def day2_part2_test1():
    cmds = ["forward 5", "down 5", "forward 8", "up 3", "down 8", "forward 2"]
    pos = PositionPart2(0, 0)
    apply_cmds(pos, cmds)
    return pos

print(f"Day2 Part1 Test1: {day2_part2_test1()}")

def day2_part2():
    puzzle = Puzzle(year = 2021, day = 2)
    cmds = puzzle.input_data.split("\n")
    pos = PositionPart2(0, 0)
    apply_cmds(pos, cmds)
    return pos.product()

print(f"Day2 Part2: {day2_part2()}")
