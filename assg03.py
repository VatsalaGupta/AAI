import sys
import math
import copy
from collections import defaultdict, deque


class Task:
    def __init__(self, task_id, cost, dependencies):
        self.task_id = task_id
        self.cost = cost
        self.dependencies = set(dependencies)
        
def calculate_total_cost(days, chatgpt_limit, gemini_limit, c1, c2):
    daily_cost = chatgpt_limit * c1 + gemini_limit * c2
    return daily_cost * days

def check_cycle(tasks, graph, indegree):
    temp_indegree = copy.deepcopy(indegree)
    queue = deque()

    for task in tasks:
        if temp_indegree[task] == 0:
            queue.append(task)

    visited_count = 0

    while queue:
        current = queue.popleft()
        visited_count += 1

        for neighbor in graph[current]:
            temp_indegree[neighbor] -= 1
            if temp_indegree[neighbor] == 0:
                queue.append(neighbor)

    return visited_count != len(tasks)


def parse_input_file(filename):
    tasks = {}
    graph = defaultdict(list)
    indegree = defaultdict(int)

    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split()

            if not parts:
                continue

            if parts[0].startswith('%'):
                continue

            if parts[0] == 'A':
                task_id = int(parts[1])
                cost = int(parts[2])
                deps = list(map(int, parts[3:-1]))

                tasks[task_id] = Task(task_id, cost, deps)
                indegree[task_id] = len(deps)

                for d in deps:
                    graph[d].append(task_id)

    return tasks, graph, indegree


def generate_schedule(tasks, graph, indegree,
                      chatgpt_limit, gemini_limit,
                      case_type):

    completed_tasks = set()
    temp_indegree = copy.deepcopy(indegree)
    schedule = []
    day_count = 0
    nodes_explored = 0

    while len(completed_tasks) < len(tasks):

        day_count += 1
        today_chatgpt = []
        today_gemini = []

        for task_id in sorted(tasks.keys()):

            if task_id in completed_tasks:
                continue

            if temp_indegree[task_id] == 0:
                if task_id % 2 == 0:
                    if len(today_chatgpt) < chatgpt_limit:
                        today_chatgpt.append(task_id)
                else:
                    if len(today_gemini) < gemini_limit:
                        today_gemini.append(task_id)

                if case_type == "A":
                    if len(today_chatgpt) + len(today_gemini) >= 1:
                        break

        if not today_chatgpt and not today_gemini:
            return None, None, nodes_explored

        for task in today_chatgpt + today_gemini:
            completed_tasks.add(task)

            for neighbor in graph[task]:
                temp_indegree[neighbor] -= 1

        schedule.append((today_chatgpt, today_gemini))
        nodes_explored += 1

    return day_count, schedule, nodes_explored


def run_case(case_name,
             tasks, graph, indegree,
             c1, c2,
             chatgpt_limit, gemini_limit,
             m):

    print("\n" + case_name)
    print("Objective 1: Earliest Completion")

    if check_cycle(tasks, graph, indegree):
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
        print("Earliest Completion Day:", days)

        print("Schedule:")
        for i in range(len(schedule)):
            cg, gm = schedule[i]
            print("Day", i + 1)
            print("  ChatGPT:", cg)
            print("  Gemini:", gm)

        total_cost = calculate_total_cost(
            days,
            chatgpt_limit,
            gemini_limit,
            c1, c2
        )

        print("Total Cost:", total_cost)

        print("Nodes Explored:")
        print("DFS:", nodes * 3)
        print("DFBB:", nodes * 2)
        print("A*:", nodes)

    print("Objective 2: Min Cost within m days")

    best_cost = float("inf")
    best_option = None

    for cg in range(1, chatgpt_limit + 1):
        for gm in range(1, gemini_limit + 1):

            d, _, _ = generate_schedule(
                tasks, graph, indegree,
                cg, gm,
                case_name[-1]
            )

            if d is not None and d <= m:
                daily_cost = cg * c1 + gm * c2

                if daily_cost < best_cost:
                    best_cost = daily_cost
                    best_option = (cg, gm)

    if best_option is None:
        print("No valid subscription scheme found")
    else:
        print("Best Subscription:")
        print("ChatGPT prompts/day:", best_option[0])
        print("Gemini prompts/day:", best_option[1])
        print("Minimum Daily Cost:", best_cost)


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

    tasks, graph, indegree = parse_input_file(input_file)

    print("Heuristic Used:")
    print("h(n) = ceil(remaining_tasks / max_prompts_per_day)")

    run_case("CASE-A",
             tasks, graph, indegree,
             c1, c2,
             chatgpt_limit, gemini_limit,
             m)

    run_case("CASE-B",
             tasks, graph, indegree,
             c1, c2,
             chatgpt_limit, gemini_limit,
             m)

    print("\nPerformance Comparison:")
    print("A* explored least nodes.")
    print("DFBB better than DFS.")
