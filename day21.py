from aocd.models import Puzzle

def puzzle_input_data():
    puzzle = Puzzle(year = 2021, day = 21)
    return puzzle.input_data

enable_debug_logging = False
def debug_log(str):
    if enable_debug_logging:
        print(f"debug: {str}")

def process_input_data(input_data):
    lines = input_data.splitlines()
    (_, player_num, _, _, player1_pos) = lines[0].split()
    assert int(player_num) == 1
    player1_pos = int(player1_pos)
    (_, player_num, _, _, player2_pos) = lines[1].split()
    assert int(player_num) == 2
    player2_pos = int(player2_pos)
    return player1_pos, player2_pos

def move_space(start, distance):
    return ((start - 1) + distance) % 10 + 1

#print(move_space(8, 4+5+6))

class DeterministicDice:
    def __init__(self):
        self.next_roll = 1
        self.num_rolls = 0
    def roll(self):
        roll = self.next_roll
        self.next_roll = (self.next_roll % 100) + 1
        self.num_rolls += 1
        return roll
    def roll_three(self):
        roll = self.roll()
        roll += self.roll()
        roll += self.roll()
        return roll
    def get_num_rolls(self):
        return self.num_rolls

def practice_game(p1_starting_pos, p2_starting_pos):
    dice = DeterministicDice()
    p1_score = 0
    p2_score = 0
    p1_pos = p1_starting_pos
    p2_pos = p2_starting_pos
    #
    while True:
        p1_pos = move_space(p1_pos, dice.roll_three())
        p1_score += p1_pos
        if p1_score >= 1000:
            break
        p2_pos = move_space(p2_pos, dice.roll_three())
        p2_score += p2_pos
        if p2_score >= 1000:
            break
    return min(p1_score, p2_score) * dice.get_num_rolls()

print(f"Practice game with example input: {practice_game(4, 8)}")

p1_starting_pos, p2_starting_pos = process_input_data(puzzle_input_data())
print(f"Practice game with puzzle input: {practice_game(p1_starting_pos, p2_starting_pos)}")

dirac_3_rolls = []
for i in (1, 2, 3):
    for j in (1, 2, 3):
        for k in (1, 2, 3):
            dirac_3_rolls.append(i + j + k)

def dirac_game(p1_starting_pos, p2_starting_pos):
    p1_roll_memo = {}
    def p1_roll_helper(p1_pos, p1_score, p2_pos, p2_score):
        if (p1_pos, p1_score, p2_pos, p2_score) in p1_roll_memo:
            return p1_roll_memo[(p1_pos, p1_score, p2_pos, p2_score)]
        if p2_score >= 21:
            return (0, 1)
        p1_total_wins = 0
        p2_total_wins = 0
        for i in dirac_3_rolls:
            p1_next_pos = move_space(p1_pos, i)
            p1_next_score = p1_score + p1_next_pos
            (p1_wins, p2_wins) = p2_roll_helper(p1_next_pos, p1_next_score, p2_pos, p2_score)
            p1_total_wins += p1_wins
            p2_total_wins += p2_wins
        p1_roll_memo[(p1_pos, p1_score, p2_pos, p2_score)] = (p1_total_wins, p2_total_wins)
        return (p1_total_wins, p2_total_wins)

    p2_roll_memo = {}
    def p2_roll_helper(p1_pos, p1_score, p2_pos, p2_score):
        if (p1_pos, p1_score, p2_pos, p2_score) in p2_roll_memo:
            return p2_roll_memo[(p1_pos, p1_score, p2_pos, p2_score)]
        if p1_score >= 21:
            return (1, 0)
        p1_total_wins = 0
        p2_total_wins = 0
        for i in dirac_3_rolls:
            p2_next_pos = move_space(p2_pos, i)
            p2_next_score = p2_score + p2_next_pos
            (p1_wins, p2_wins) = p1_roll_helper(p1_pos, p1_score, p2_next_pos, p2_next_score)
            p1_total_wins += p1_wins
            p2_total_wins += p2_wins
        p2_roll_memo[(p1_pos, p1_score, p2_pos, p2_score)] = (p1_total_wins, p2_total_wins)
        return (p1_total_wins, p2_total_wins)

    (p1_wins, p2_wins) = p1_roll_helper(p1_starting_pos, 0, p2_starting_pos, 0)
    return max(p1_wins, p2_wins)

print(f"Dirac dice game with example input: {dirac_game(4, 8)}")
print(f"Dirac dice game with puzzle input: {dirac_game(p1_starting_pos, p2_starting_pos)}")
