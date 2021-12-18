from aocd.models import Puzzle

# fixed values
DIM = 5

class BoardCell:
    def __init__(self, number):
        self.number = number
        self.is_marked = False
    def mark(self):
        self.is_marked = True

class Board:
    def __init__(self, board_vals):
        self.board_cells = []
        self.winning_num = None
        for row in board_vals:
            board_cell_row = [BoardCell(int(num)) for num in row]
            self.board_cells.append(board_cell_row)
    def find(self, number):
        if not isinstance(number, int):
            raise Exception("integer is expected")
        matches = []
        for row in self.board_cells:
            for cell in row:
                if cell.number == number:
                    matches.append(cell)
        return matches
    def mark(self, drawn_number):
        if not isinstance(drawn_number, int):
            raise Exception("integer is expected")
        matches = self.find(drawn_number)
        for match in matches:
            match.mark()
        # Check if the latest marked number makes us a winner
        # and record the winning number
        if self.winning_num != None:
            raise Exception("attempt to mark more numbers after a win!")
        # Check for a winning row
        for row_idx in range(0, DIM):
            markings = 0
            for col_idx in range(0, DIM):
                if self.board_cells[row_idx][col_idx].is_marked:
                    markings += 1
            if markings == DIM:
                self.winning_num = drawn_number
                break
        if self.winning_num != None:
            # already found a win via row
            return
        # Check for a winning column
        for col_idx in range(0, DIM):
            markings = 0
            for row_idx in range(0, DIM):
                if self.board_cells[row_idx][col_idx].is_marked:
                    markings += 1
            if markings == DIM:
                self.winning_num = drawn_number
                break
    def is_winner(self):
        return self.winning_num != None
    def score(self):
        if self.winning_num == None:
            return None
        # Get the sum of all unmarked numbers
        unmarked_sum = 0
        for row in self.board_cells:
            for cell in row:
                if not cell.is_marked:
                    unmarked_sum += cell.number
        return self.winning_num * unmarked_sum

def find_winning_score(drawn_nums, boards):
    for drawn_num in drawn_nums:
        for board_idx, board in enumerate(boards):
            board.mark(drawn_num)
            if board.is_winner():
                print(f"DEBUG: Winning Number is {drawn_num}")
                print(f"DEBUG: Winning Board is {board_idx}")
                assert board.winning_num == drawn_num
                return board.score()

def find_last_winners_score(drawn_nums, boards):
    last_winning_board_idx = None
    num_remaining_to_win = len(boards)
    for drawn_num in drawn_nums:
        if num_remaining_to_win == 0:
            break
        for board_idx, board in enumerate(boards):
            if board.is_winner():
                continue
            board.mark(drawn_num)
            if board.is_winner():
                assert board.winning_num == drawn_num
                # Last one so far to win
                last_winning_board_idx = board_idx
                num_remaining_to_win -= 1
    
    print(f"DEBUG: Last winning Board is {last_winning_board_idx} with winning number {boards[last_winning_board_idx].winning_num}")
    return boards[last_winning_board_idx].score()


def process_input(lines):
    drawn_nums = [int(x) for x in lines[0].split(",")]
    # Series of blank line followed by DIM rows of board
    board_vals_list = []
    for line_idx in range(1, len(lines), DIM + 1):
        if lines[line_idx] != "":
            raise Exception(f"missing blank line at line number: {line_idx}")
        # lines from line_idx+1 to line_idx+5 are rows of numbers
        board_vals = []
        for board_row_idx in range(DIM):
            board_row = []
            for val_str in lines[line_idx + board_row_idx + 1].split():
                board_row.append(int(val_str))
            board_vals.append(board_row)
        board_vals_list.append(board_vals)
    boards = []
    for board_vals in board_vals_list:
        boards.append(Board(board_vals))
    return drawn_nums, boards

def day4_board_data():
    puzzle = Puzzle(year = 2021, day = 4)
    input = puzzle.input_data.split("\n")
    return process_input(input)

test_input_lines1 = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""

def test_input_data():
    input = test_input_lines1.split("\n")
    return process_input(input)

def day4_part1_test1():
    drawn_nums, boards = test_input_data()
    winning_score = find_winning_score(drawn_nums, boards)
    print(f"Day4 Part1 Winning Score = {winning_score}")

day4_part1_test1()

def day4_part1():
    drawn_nums, boards = day4_board_data()
    return find_winning_score(drawn_nums, boards)

day4_part1()

def day4_part2_test1():
    drawn_nums, boards = test_input_data()
    winning_score = find_last_winners_score(drawn_nums, boards)
    print(f"Day4 Part2 Test Last Winning Score = {winning_score}")

day4_part2_test1()

def day4_part2():
    drawn_nums, boards = day4_board_data()
    winning_score = find_last_winners_score(drawn_nums, boards)
    print(f"Day4 Part2 Last Winning Score = {winning_score}")

day4_part2()
