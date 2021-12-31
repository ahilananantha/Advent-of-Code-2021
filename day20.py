from aocd.models import Puzzle

def puzzle_input_data():
    puzzle = Puzzle(year = 2021, day = 20)
    return puzzle.input_data

enable_debug_logging = False
def debug_log(str):
    if enable_debug_logging:
        print(f"debug: {str}")

def process_input_data(input_data):
    lines = input_data.splitlines()
    # first line is the image enhancement algorithm
    algo = lines[0]
    input_image = []
    for idx in range(2, len(lines)):
        input_image.append(list(lines[idx]))
    return algo, input_image

def enhance_pixel(algo, input_image, input_i, input_j, outer_value):
    pixel_str = []
    nrows = len(input_image)
    ncols = len(input_image[0])
    for i in (input_i - 1, input_i, input_i + 1):
        for j in (input_j - 1, input_j, input_j + 1):
            if (0 <= i < nrows) and (0 <= j < ncols):
                pixel_str.append(input_image[i][j])
            else:
                pixel_str.append(outer_value)
    algo_index = 0
    for i in range(0, len(pixel_str)):
        if pixel_str[i] == '#':
            algo_index |= 0x1 << (len(pixel_str) - 1 - i)
    return algo[algo_index]

def enhance_image(algo, input_image, outer_value):
    # image grows by a pixel around the original image
    output_image = []
    nrows = len(input_image)
    ncols = len(input_image[0])
    for i in range(-1, nrows + 1):
        new_row = []
        for j in range(-1, ncols + 1):
            new_row.append(enhance_pixel(algo, input_image, i, j, outer_value))
        output_image.append(new_row)
    if outer_value == '#':
        # all ones
        next_outer_value = algo[-1]
    else:
        # all zeroes
        next_outer_value = algo[0]
    return output_image, next_outer_value

def display_image(image):
    for i in range(0, len(image)):
        print("".join(image[i]))

def num_lit(image):
    count = 0
    for i in range(0, len(image)):
        for j in range(0, len(image[0])):
            if image[i][j] == "#":
                count += 1
    return count


test_algo = """\
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##\
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###\
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.\
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....\
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..\
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....\
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#\
"""

print(len(test_algo))

test_input_image_str="""\
#..#.
#....
##..#
..#..
..###\
"""

test_input_image = []
for image_line in test_input_image_str.splitlines():
    test_input_image.append(list(image_line))

#print(enhance_pixel(test_algo, test_input_image, 0, 0, "."))

def get_num_lit_double_enhance(algo, input_image):
    print("Input image:")
    display_image(input_image)
    print()
    # initially all other pixels outside the image are unlit
    outer_value = "."
    output_image, next_outer_value = enhance_image(algo, input_image, outer_value)
    print("After one enhance:")
    display_image(output_image)
    print()
    print("Outside the image the pixels are all: " + next_outer_value)
    second_image, second_outer_value = enhance_image(algo, output_image, next_outer_value)
    print("After second enhance:")
    display_image(second_image)
    print()
    print("Outside the image the pixels are all: " + second_outer_value)
    # Otherwise infinite pixels are lit!
    assert second_outer_value == "."
    return num_lit(second_image)

test_num_lit = get_num_lit_double_enhance(test_algo, test_input_image)
print(f"Num lit pixels in example input after double enhance: {test_num_lit}")

puzzle_algo, puzzle_image = process_input_data(puzzle_input_data())
puzzle_num_lit = get_num_lit_double_enhance(puzzle_algo, puzzle_image)
print(f"Num lit pixels in puzzle input after double enhance: {puzzle_num_lit}")

def get_num_lit_multi_enhance(algo, input_image, num_enhancements):
    # initially all other pixels outside the image are unlit
    image = input_image
    outer_value = "."
    for i in range(0, num_enhancements):
        image, outer_value = enhance_image(algo, image, outer_value)
    print("Outside the image the pixels are all: " + outer_value)
    # Otherwise infinite pixels are lit!
    assert outer_value == "."
    return num_lit(image)

test_num_lit = get_num_lit_multi_enhance(test_algo, test_input_image, 50)
print(f"Num lit pixels in example input after 50 enhances: {test_num_lit}")

puzzle_num_lit = get_num_lit_multi_enhance(puzzle_algo, puzzle_image, 50)
print(f"Num lit pixels in puzzle input after 50 enhances: {puzzle_num_lit}")
