from aocd.models import Puzzle

test_input_data1 = """\
start-A
start-b
A-c
A-b
b-d
A-end
b-end\
"""

def day12_input_data():
    puzzle = Puzzle(year = 2021, day = 12)
    return puzzle.input_data

def process_input_data(input_data):
    # Return adjacency list for undirected graph
    adjList = {}
    lines = input_data.splitlines()
    for line in lines:
        (from_vertex, to_vertex) = line.split("-")
        if from_vertex not in adjList:
            adjList[from_vertex] = []
        if to_vertex not in adjList:
            adjList[to_vertex] = []
        adjList[from_vertex].append(to_vertex)
        adjList[to_vertex].append(from_vertex)
    return adjList

test_input_graph1 = process_input_data(test_input_data1)
#print(test_input_graph1)

# can visit large caves more than once, small caves at most once
# it looks like there's never a large cave connected to another large cave
def find_all_paths_part1(graph):
    paths = []

    def is_small_cave(node):
        return node.islower()

    def is_repetitive(path_so_far, node):
        if is_small_cave(node):
            # small cave or start/end,  can only visit them once
            return node in path_so_far
        else:
            # can visit a large cave as many times as we want
            return False

    def find_paths_to_end(node, path_so_far):
        if node == "end":
            path_so_far.append(node)
            paths.append(path_so_far[:])
            path_so_far.pop()
            return
        for neighbor in graph[node]:
            path_so_far.append(node)
            if not is_repetitive(path_so_far, neighbor):
                find_paths_to_end(neighbor, path_so_far)
            path_so_far.pop()
    
    find_paths_to_end("start", [])
    return paths

def pretty_print_paths(paths):
    print(f"{len(paths)} paths found")
    for path in paths:
        print(",".join(path))
    print("")

#pretty_print_paths(find_all_paths_part1(test_input_graph1))
print(len(find_all_paths_part1(test_input_graph1)))

test_input_data2 = """\
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc\
"""

test_input_graph2 = process_input_data(test_input_data2)
#pretty_print_paths(find_all_paths_part1(test_input_graph2))
print(len(find_all_paths_part1(test_input_graph2)))

test_input_data3 = """\
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW\
"""

test_input_graph3 = process_input_data(test_input_data3)
#pretty_print_paths(find_all_paths_part1(test_input_graph3))
print(len(find_all_paths_part1(test_input_graph3)))

day12_graph = process_input_data(day12_input_data())
print(f"Day 12 (part 1) number of paths: {len(find_all_paths_part1(day12_graph))}")

def find_all_paths_part2(graph):
    paths = []

    def is_large_cave(node):
        return node.isupper()
    def is_small_cave(node):
        # start and end have different requirements now
        return node.islower() and node != "start" and node != "end"

    def is_repetitive(path_so_far, node):
        if is_large_cave(node):
            # can visit a large cave any number of times
            return False
        elif is_small_cave(node):
            # can visit one small cave twice, the others once
            freq = {}
            hit_cap = False
            for x in path_so_far:
                if is_small_cave(x):
                    freq[x] = freq.get(x, 0) + 1
                    if freq[x] == 2:
                        hit_cap = True
            if node not in freq:
                # Never visited this small cave before
                return False
            if hit_cap:
                # One cave already was repeated
                return True
        else:
            # start or end, can only visit once
            return node in path_so_far

    def find_paths_to_end(node, path_so_far):
        if node == "end":
            path_so_far.append(node)
            paths.append(path_so_far[:])
            path_so_far.pop()
            return
        for neighbor in graph[node]:
            path_so_far.append(node)
            if not is_repetitive(path_so_far, neighbor):
                find_paths_to_end(neighbor, path_so_far)
            path_so_far.pop()
    
    find_paths_to_end("start", [])
    return paths

print(len(find_all_paths_part2(test_input_graph1)))
print(len(find_all_paths_part2(test_input_graph2)))
print(len(find_all_paths_part2(test_input_graph3)))

print(f"Day 12 (part 2) number of paths: {len(find_all_paths_part2(day12_graph))}")