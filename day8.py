from aocd.models import Puzzle

correct_signal_patterns = [
    ["a", "b", "c", "e", "f", "g"],
    ["c", "f"],
    ["a", "c", "d", "e", "g"],
    ["a", "c", "d", "f", "g"],
    ["b", "c", "d", "f"],
    ["a", "b", "d", "f", "g"],
    ["a", "b", "d", "e", "f", "g"],
    ["a", "c", "f"],
    ["a", "b", "c", "d", "e", "f", "g"],
    ["a", "b", "c", "d", "f", "g"]
]

def day8_input_data():
    puzzle = Puzzle(year = 2021, day = 8)
    return puzzle.input_data

def process_input_data(input_data):
    lines = input_data.split("\n")
    data = []
    for line in lines:
        words = line.split()
        # find the "|" word
        i = 0
        while words[i] != "|":
            i += 1
        # is the index of "|"
        unique_digit_signals = words[0:i]
        output_digit_signals = words[i+1:len(words)]
        data.append((unique_digit_signals, output_digit_signals))
    return data

test_input_data = """\
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce\
"""

test_processed = process_input_data(test_input_data)
#print(test_processed)

def find_some(entries):
    counts = [0] * 10
    for (unique_digit_signals, output_digit_signals) in entries:
        for output_digit_signal in output_digit_signals:
            for i in (1, 4, 7, 8):
                if len(output_digit_signal) == len(correct_signal_patterns[i]):
                    counts[i] += 1
    return sum(counts)

print(find_some(test_processed))

puzzle_processed = process_input_data(day8_input_data())

print(find_some(puzzle_processed))

# 0 : a, b, c, e, f g
# 1 : c, f
# 2 : a, c, d, e, g
# 3 : a, c, d, f, g
# 4 : b, c, d, f
# 5 : a, b, d, f, g
# 6 : a, b, d, e, f, g
# 7 : a, c, f
# 8 : a, b, c, d, e, f, g
# 9 : a, b, c, d, f, g

# 1 : (a, b) -> (c, f)
# 4 : (e, a, f, b) -> (b, c, d, f)
# 7 : (d, a, b) -> (a, c, f)

# 8 is the one where len is 7
# 9 is one where len is 6, and letters(4) is a subset of it
# 6 is one where len is 6, and letters(4) is NOT a subset of it, and letters of 7 is NOT a subset of it
# 0 is one where len is 6, and letters(4) is NOT a subset of it, and letters of 7 is is subset ot it

# still to figure out:
# 5 is one where len is 5, and letters(5) is a subset of letters(6)
# 2 is one where len is 5, and letters(2) is not a subset of letters(6), is not a subset of letters(9) 
# 3 is one where len is 5, and letters(3) is not a subset of letters(6), is a subset of letters(9)


def identify_digit_patterns(patterns):
    digit_pattern_sets = [None] * 10
    pattern_sets = []
    for pattern in patterns:
        pattern_sets.append(set([x for x in pattern]))
    # First pass: can identify 1, 4, 7, 8
    for i in range(0, 10):
        # 1
        if len(pattern_sets[i]) == 2:
            digit_pattern_sets[1] = pattern_sets[i]
        # 4
        if len(pattern_sets[i]) == 4:
            digit_pattern_sets[4] = pattern_sets[i]
        # 7
        if len(pattern_sets[i]) == 3:
            digit_pattern_sets[7] = pattern_sets[i]
        # 8
        if len(pattern_sets[i]) == 7:
            digit_pattern_sets[8] = pattern_sets[i]
    # Second pass, can figure out 0, 6, 9
    for i in range(0, 10):
        if len(pattern_sets[i]) == 6:
            # 9
            if digit_pattern_sets[4].issubset(pattern_sets[i]):
                digit_pattern_sets[9] = pattern_sets[i]
            else:
                # 0
                if digit_pattern_sets[7].issubset(pattern_sets[i]):
                    digit_pattern_sets[0] = pattern_sets[i]
                # 6
                else:
                    digit_pattern_sets[6] = pattern_sets[i]
    # Third pass, can figure out 2, 3, 5
    for i in range(0, 10):
        if len(pattern_sets[i]) == 5:
            # 5
            if pattern_sets[i].issubset(digit_pattern_sets[6]):
                digit_pattern_sets[5] = pattern_sets[i]
            else:
                # 3
                if pattern_sets[i].issubset(digit_pattern_sets[9]):
                    digit_pattern_sets[3] = pattern_sets[i]
                # 2
                else:
                    digit_pattern_sets[2] = pattern_sets[i]
    return digit_pattern_sets

test_input_one_line = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"

test_processed_one_line = test_processed[0]

digit_pattern_sets = identify_digit_patterns(test_processed_one_line[0])
for i in range(0, 10):
    word = "".join(list(digit_pattern_sets[i]))
    print(f"{i}: {word}")
#print(digit_patterns_sets)

def decode_digits(digit_pattern_sets, output_signals):
    output_digits = []
    for output_signal in output_signals:
        output_set = set([x for x in output_signal])
        for i, x in enumerate(digit_pattern_sets):
            if output_set == x:
                output_digits.append(i)
    num = 0
    for i in range(0, len(output_digits)):
        num = 10*num + output_digits[i]
    return num

print(decode_digits(digit_pattern_sets, test_processed_one_line[1]))

def decode_entry(unique_digit_signals, output_digit_signals):
    digit_pattern_sets = identify_digit_patterns(unique_digit_signals)
    number = decode_digits(digit_pattern_sets, output_digit_signals)
    print(f"{unique_digit_signals}: {number}")
    return number

def decode_entries(entries):
    sum = 0
    for (unique_digit_signals, output_digit_signals) in entries:
        sum += decode_entry(unique_digit_signals, output_digit_signals)
    return sum

print(f"sum: {decode_entries(test_processed)}")


print(f"sum: {decode_entries(puzzle_processed)}")