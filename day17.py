from aocd.models import Puzzle
import math
from collections import defaultdict

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
print(f"Highest Y value for puzzle input: {highest_y(target_y_range)}")

def solve_quadratic(a, b, c):
    # discriminant
    d = (b**2) - (4*a*c)
    # Only care about real roots
    if d < 0:
        return None
    elif d == 0:
        return [-b/(2*a)]
    else:
        # one root is negative
        return [(-b - math.sqrt(d)) / (2*a),
                (-b + math.sqrt(d)) / (2 * a)]

def get_minimum_x_velocity(x_min_distance):
    # because of drag of -1, this is an arithmetic series of positive
    # integers with delta of 1. the furthest distance for a given
    # initial velocity is the series sum from 1 to initial_v.
    # x_min_distance = v(v + 1)/2
    # solve for v using quadratic formula. we discard negative
    # initial v quadratic solution as invalid.
    roots = solve_quadratic(0.5, 0.5, -x_min_distance)
    for root in roots:
        if root > 0:
            # round up since we can overshoot but not undershoot
            return int(root + 0.5)

def initial_x_velocities(target_x_min, target_x_max, max_steps):
    #maximum initial x velocity is x_max, where after a single
    #step we reach the end of the target area.
    max_v = target_x_max
    min_v = get_minimum_x_velocity(target_x_min)
    step_x_vel = defaultdict(list)
    for initial_v in range(min_v, max_v + 1):
        v = initial_v
        d = 0
        steps = 0
        while d < target_x_max:
            d += v
            steps += 1
            if target_x_min <= d <= target_x_max:
                step_x_vel[steps].append(initial_v)
            if v > 0:
                v -= 1
            else:
                if d < target_x_min:
                    # won't reach it ever if v is 0
                    break
                elif steps >= max_steps:
                    # x distance will stay forever so need to avoid
                    # infinite loop.
                    break
    return step_x_vel

def initial_y_velocities(target_y_min, target_y_max):
    max_v = -target_y_min - 1
    min_v = target_y_min
    max_steps = 0
    step_y_vel = defaultdict(list)
    for initial_v in range(min_v, max_v + 1):
        v = initial_v
        d = 0
        steps = 0
        while d > target_y_min:
            d += v
            steps += 1
            if target_y_min <= d <= target_y_max:
                step_y_vel[steps].append(initial_v)
                max_steps = max(max_steps, steps)
            v -= 1
    return (step_y_vel, max_steps)

def initial_velocities(xrange, yrange):
    (step_y, max_steps) = initial_y_velocities(yrange[0], yrange[1])
    step_x = initial_x_velocities(xrange[0], xrange[1], max_steps)
    velocities = set()
    for step in step_x:
        if step in step_y:
            # intersect
            vels_x = step_x[step]
            vels_y = step_y[step]
            for vel_x in vels_x:
                for vel_y in vels_y:
                    velocities.add((vel_x, vel_y))
    return sorted(list(velocities))

print(f"Number of distinct initial velocities for test input: {len(initial_velocities([20, 30], [-10, -5]))}")
print(f"Number of distinct initial velocities for puzzle input: {len(initial_velocities(target_xrange, target_y_range))}")
