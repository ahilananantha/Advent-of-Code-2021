from aocd.models import Puzzle


def puzzle_input_data():
    puzzle = Puzzle(year = 2021, day = 17)
    return puzzle.input_data

def process_input_data(input_data):
    lines = input_data.splitlines()
    assert len(lines) == 1
    (_, _, xrange_s, yrange_s) = lines[0].split()
    (xrange_min_s, xrange_max_s) = xrange_s.split(",")[0].split("=")[1].split("..")
    (yrange_min_s, yrange_max_s) = yrange_s.split("=")[1].split("..")
    xrange = (int(xrange_min_s), int(xrange_max_s))
    yrange = (int(yrange_min_s), int(yrange_max_s))
    return (xrange, yrange)

print(process_input_data(puzzle_input_data()))

# at the bottom of trajectory (y = 0) velocity will be negative of the
# original velocity. then it will go down by 1 as the target is below
# us. if the bottom of the target is at -20, that means velocities at
# y = 0 will be 19 and -19. height is sum of 1..19. that means
# height is sum 1..(-target_ymin - 1) 

def highest_y(target_yrange):
    target_ymin = target_yrange[0]
    series_end = -target_ymin - 1
    return (series_end)*(series_end + 1) // 2

(target_xrange, target_y_range) = process_input_data(puzzle_input_data())
print(highest_y(target_y_range))
