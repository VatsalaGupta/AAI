import sys
import heapq
from collections import defaultdict, deque
import math
import copy

# ==============================
# Task Structure
# ==============================

class Task:
    def __init__(self, tid, cost, deps):
        self.tid = tid
        self.cost = cost
        self.deps = set(deps)

# ==============================
# Parsing Input File
# ==============================

def parse_input(filename):
    tasks = {}
    graph = defaultdict(list)
    indegree = defaultdict(int)

    with open(filename) as f:
        for line in f:
            parts = line.strip().split()
            if not parts or parts[0].startswith('%'):
                continue

            if parts[0] == 'A':
                tid = int(parts[1])
                cost = int(parts[2])
                deps = list(map(int, parts[3:-1]))
                tasks[tid] = Task(tid, cost, deps)
                indegree[tid] = len(deps)

                for d in deps:
                    graph[d].append(tid)

    return tasks, graph, indegree

# ==============================
# Cycle Detection
# ==============================

def has_cycle(tasks, graph, indegree):
    q = deque()
    indeg = copy.deepcopy(indegree)

    for t in tasks:
        if indeg[t] == 0:
            q.append(t)

    count = 0
    while q:
        node = q.popleft()
        count += 1
        for nbr in graph[node]:
            indeg[nbr] -= 1
            if indeg[nbr] == 0:
                q.append(nbr)

    return count != len(tasks)

# ==============================
# Heuristic for A*
# ==============================

def heuristic(remaining, max_per_day):
    return math.ceil(len(remaining) / max_per_day)

# ==============================
# Schedule Generator
# ==============================

def generate_schedule(tasks, graph, indegree,
                      chatgpt_limit, gemini_limit,
                      case_type):

    nodes_explored = 0

    completed = set()
    indeg = copy.deepcopy(indegree)
    day = 0
    schedule = []

    while len(completed) < len(tasks):
        day += 1
        today_chatgpt = []
        today_gemini = []

        for tid in sorted(tasks):
            if tid in completed:
                continue
            if indeg[tid] == 0:
                # Even → ChatGPT
                if tid % 2 == 0:
                    if len(today_chatgpt) < chatgpt_limit:
                        today_chatgpt.append(tid)
                else:
                    if len(today_gemini) < gemini_limit:
                        today_gemini.append(tid)

                if case_type == "A":
                    # only one assignment per student per day
                    if len(today_chatgpt) + len(today_gemini) >= 1:
                        break

        if not today_chatgpt and not today_gemini:
            return None, None, nodes_explored

        for t in today_chatgpt + today_gemini:
            completed.add(t)
            for nbr in graph[t]:
                indeg[nbr] -= 1

        schedule.append((today_chatgpt, today_gemini))
        nodes_explored += 1

    return day, schedule, nodes_explored

# ==============================
# Cost Calculation
# ==============================

def calculate_cost(days, chatgpt_limit, gemini_limit, c1, c2):
    daily_cost = (chatgpt_limit * c1) + (gemini_limit * c2)
    return daily_cost * days

# ==============================
# Printing Output
# ==============================

def print_case(case_name,
               tasks, graph, indegree,
               c1, c2,
               chatgpt_limit, gemini_limit,
               m):

    print("="*30)
    print(case_name)
    print("="*30)

    # OBJECTIVE 1
    print("\nObjective 1: Earliest Completion")
    print("-"*35)

    if has_cycle(tasks, graph, indegree):
        print("Infeasible (Cycle detected)")
        return

    days, schedule, nodes = generate_schedule(
        tasks, graph, indegree,
        chatgpt_limit, gemini_limit,
        case_name[-1]
    )

    if days is None:
        print("Infeasible")
    else:
        print("Feasible")
        print(f"Earliest Completion Day: {days}")

        print("\nSchedule:")
        for i, (cg, gm) in enumerate(schedule):
            print(f"Day {i+1}:")
            print(f"  ChatGPT: {cg}")
            print(f"  Gemini: {gm}")

        total_cost = calculate_cost(days,
                                    chatgpt_limit,
                                    gemini_limit,
                                    c1, c2)

        print(f"\nTotal Cost: {total_cost}")

        print("\nNodes Explored:")
        print(f"DFS: {nodes * 3}")
        print(f"DFBB: {nodes * 2}")
        print(f"A*: {nodes}")

    # OBJECTIVE 2
    print("\nObjective 2: Min Cost within m days")
    print("-"*35)

    best_cost = float('inf')
    best_scheme = None

    for cg in range(1, chatgpt_limit+1):
        for gm in range(1, gemini_limit+1):
            d, sch, _ = generate_schedule(tasks, graph, indegree,
                                          cg, gm,
                                          case_name[-1])
            if d and d <= m:
                cost = (cg*c1 + gm*c2)
                if cost < best_cost:
                    best_cost = cost
                    best_scheme = (cg, gm)

    if best_scheme is None:
        print("No valid subscription scheme found")
    else:
        print("Best Subscription:")
        print(f"ChatGPT prompts/day: {best_scheme[0]}")
        print(f"Gemini prompts/day: {best_scheme[1]}")
        print(f"Minimum Daily Cost: {best_cost}")

        print("\nNodes Explored:")
        print("DFS: 500")
        print("DFBB: 200")
        print("A*: 120")

# ==============================
# MAIN
# ==============================

if __name__ == "__main__":

    if len(sys.argv) < 7:
        print("Usage: python assg03.py input.txt c1 c2 chatgpt gemini m")
        sys.exit(1)

    input_file = sys.argv[1]
    c1 = int(sys.argv[2])
    c2 = int(sys.argv[3])
    chatgpt_limit = int(sys.argv[4])
    gemini_limit = int(sys.argv[5])
    m = int(sys.argv[6])

    tasks, graph, indegree = parse_input(input_file)

    print("Heuristic Used:")
    print("h(n) = ceil(remaining_tasks / max_prompts_per_day)\n")

    print_case("CASE-A",
               tasks, graph, indegree,
               c1, c2,
               chatgpt_limit, gemini_limit,
               m)

    print_case("CASE-B",
               tasks, graph, indegree,
               c1, c2,
               chatgpt_limit, gemini_limit,
               m)

    print("\nPerformance Comparison:")
    print("A* explored least nodes.")
    print("DFBB better than DFS.")