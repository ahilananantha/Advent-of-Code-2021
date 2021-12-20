from aocd.models import Puzzle

test_input_data = """\
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]\
"""

def day10_input_data():
    puzzle = Puzzle(year = 2021, day = 10)
    return puzzle.input_data

def process_input_data(input_data):
    return input_data.splitlines()

def validate_chunk(chunk_str):
    def closing_for(c):
        if c == "(":
            return ")"
        elif c == "[":
            return "]"
        elif c == "{":
            return "}"
        elif c == "<":
            return ">"
        return None

    def is_closing(c):
        return c == ")" or c == "]" or c == "}" or c == ">"
    def is_opening(c):
        return c == "(" or c == "[" or c == "{" or c == "<"
    
    closing_chars = []

    def helper(chunk_arr, start):
        if start == len(chunk_arr):
            # empty is valid
            return (start, True)
        # We expect to be called on a starting character.. if not, we
        # found an error. return the index of the unexpected character.
        if is_closing(chunk_arr[start]):
            return (start, False)
        if not is_opening(chunk_arr[start]):
            raise Exception(f"invalid character: {chunk_arr[start]}")
        opening_char = chunk_arr[start]
        # the next character could close the chunk
        closing_char = closing_for(opening_char)
        while start + 1 < len(chunk_arr):
            if chunk_arr[start + 1] == closing_char:
                # Another base case for valid
                return (start + 1, True)
            # Recurse
            (end, valid) = helper(chunk_arr, start + 1)
            if not valid:
                return (end, valid)
            start = end
        # means incomplete, we treat this as not corrupt
        closing_chars.append(closing_char)
        return (start, True)

    chunk_arr = list(chunk_str)
    (end, valid) = helper(chunk_arr, 0)
    if not valid:
        return (False, chunk_arr[end], [])
    else:
        return (True, None, closing_chars)

def syntax_error_score(invalid_char):
    return {
        ")": 3,
        "]": 57,
        "}": 1197,
        ">": 25137,
    }.get(invalid_char, 0)

def calc_syntax_error_score(input_lines):
    total = 0
    for line in input_lines:
        (valid, first_invalid, closing_chars) = validate_chunk(line)
        if not valid:
            score = syntax_error_score(first_invalid)
            total += score
    return total

#print(validate_chunk("[<>[]}"))
#print(validate_chunk("{([(<{}[<>[]}>{[]{[(<()>"))

test_input_lines = process_input_data(test_input_data)
day10_input_lines = process_input_data(day10_input_data())

print(f"Test input syntax error score: {calc_syntax_error_score(test_input_lines)}")
print(f"Day 10 input syntax error score: {calc_syntax_error_score(day10_input_lines)}")

def autocomplete_score(closing_char):
    return {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4,
    }.get(closing_char, 0)

def calc_autocomplete_score(input_lines):
    all_totals = []
    for line in input_lines:
        (valid, first_invalid, closing_chars) = validate_chunk(line)
        if valid and len(closing_chars) > 0:
            line_total = 0
            for c in closing_chars:
                line_total = line_total * 5 + autocomplete_score(c)
            all_totals.append(line_total)
    if len(all_totals) == 0:
        raise Exception("expected at least one incomplete line")
    all_totals.sort()
    mid = (len(all_totals) - 1) // 2
    return all_totals[mid]

print(f"Test input autocomplete score: {calc_autocomplete_score(test_input_lines)}")
print(f"Day 10 input autocomplete score: {calc_autocomplete_score(day10_input_lines)}")
