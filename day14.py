from aocd.models import Puzzle

def day14_input_data():
    puzzle = Puzzle(year = 2021, day = 14)
    return puzzle.input_data

def process_input_data(input_data):
    lines = input_data.splitlines()
    # first line is the polymer template:
    polymer_template = lines[0]
    # followed by a blank line
    assert lines[1] == ""
    # then the pair insertion rules
    pair_insertion_rules = {}
    line_idx = 2
    while line_idx < len(lines):
        # XY -> Z
        (element_pair, arrow, inserted_element) = lines[line_idx].split()
        assert arrow == "->"
        pair_insertion_rules[(element_pair[0], element_pair[1])] = inserted_element
        line_idx += 1
    return (polymer_template, pair_insertion_rules)

def one_step_slow(polymer, pair_insertion_rules):
    output = []
    for i in range(0, len(polymer) - 1):
        output.append(polymer[i])
        p = (polymer[i], polymer[i + 1])
        if p in pair_insertion_rules:
            inserted_element = pair_insertion_rules[p]
            output.append(inserted_element)
    output.append(polymer[-1])
    return "".join(output)

def n_steps_slow(polymer_template, pair_insertion_rules, num_steps):
    polymer = polymer_template
    for i in range(0, num_steps):
        polymer = one_step_slow(polymer, pair_insertion_rules)
        #print(f"After {i+1} steps: len = {len(polymer)}: {polymer}")
    element_counts = {}
    for element in polymer:
        element_counts[element] = element_counts.get(element, 0) + 1
    lowest_count = None
    highest_count = None
    for element in element_counts:
        if lowest_count == None:
            lowest_count = element_counts[element]
        if highest_count == None:
            highest_count = element_counts[element]
        highest_count = max(highest_count, element_counts[element])
        lowest_count = min(lowest_count, element_counts[element])
    return highest_count - lowest_count

def init_counts(polymer_template):
    pair_counts = {}
    elem_counts = {}
    for i in range(0, len(polymer_template) - 1):
        p = (polymer_template[i], polymer_template[i + 1])
        pair_counts[p] = pair_counts.get(p, 0) + 1
        elem_counts[polymer_template[i]] = elem_counts.get(polymer_template[i], 0) + 1
    elem_counts[polymer_template[-1]] = elem_counts.get(polymer_template[-1], 0) + 1
    return (pair_counts, elem_counts)

def one_step(pair_counts, elem_counts, pair_insertion_rules):
    new_pair_counts = pair_counts.copy()
    new_elem_counts = elem_counts.copy()
    for (pair, count) in pair_counts.items():
        if count == 0:
            continue
        if pair in pair_insertion_rules:
            element = pair_insertion_rules[pair]
            new_pair1 = (pair[0], element)
            new_pair2 = (element, pair[1])
            new_pair_counts[pair] -= count
            new_pair_counts[new_pair1] = new_pair_counts.get(new_pair1, 0) + count
            new_pair_counts[new_pair2] = new_pair_counts.get(new_pair2, 0) + count
            new_elem_counts[element] = new_elem_counts.get(element, 0) + count
    return (new_pair_counts, new_elem_counts)

def n_steps(polymer_template, pair_insertion_rules, num_steps):
    (pair_counts, elem_counts) = init_counts(polymer_template)
    for i in range(0, num_steps):
        (pair_counts, elem_counts) = one_step(pair_counts, elem_counts, pair_insertion_rules)
    
    lowest_count = None
    highest_count = None
    for element in elem_counts:
        if lowest_count == None:
            lowest_count = elem_counts[element]
        if highest_count == None:
            highest_count = elem_counts[element]
        highest_count = max(highest_count, elem_counts[element])
        lowest_count = min(lowest_count, elem_counts[element])
    return highest_count - lowest_count

test_input_data = """\
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C\
"""

#print(process_input_data(test_input_data))
test_input_polymer_template, test_input_insertion_rules = process_input_data(test_input_data)

print(f"Test input (10 steps) slow value: {n_steps_slow(test_input_polymer_template, test_input_insertion_rules, 10)}")
print(f"Test input (10) steps) fast value: {n_steps(test_input_polymer_template, test_input_insertion_rules, 10)}")

puzzle_polymer_template, puzzle_insertion_rules = process_input_data(day14_input_data())
print(f"Puzzle input (10 steps) slow value: {n_steps_slow(puzzle_polymer_template, puzzle_insertion_rules, 10)}")
print(f"Puzzle input (10 steps) fast value: {n_steps(puzzle_polymer_template, puzzle_insertion_rules, 10)}")

print(f"Test input (40 steps) value: {n_steps(test_input_polymer_template, test_input_insertion_rules, 40)}")
print(f"Puzzle input (40 steps) fast value: {n_steps(puzzle_polymer_template, puzzle_insertion_rules, 40)}")
