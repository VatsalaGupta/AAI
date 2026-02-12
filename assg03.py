import sys
import heapq
import copy

# --- Data Structures ---
class Task:
    def __init__(self, tid, prompts, deps):
        self.tid = tid
        self.prompts = prompts
        self.deps = deps
        self.llm = "ChatGPT" if tid % 2 == 0 else "Gemini"

def parse_input(filename):
    tasks = {}
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('%'):
                continue
            parts = line.split()
            if parts[0] != 'A':
                continue
            vals = list(map(int, parts[1:]))
            if len(vals) < 2:
                continue
            tid = vals[0]
            prompts = vals[1]
            deps = [d for d in vals[2:] if d != 0]
            tasks[tid] = Task(tid, prompts, deps)
    return tasks

# --- Global Tracking for Node Comparison ---
nodes_count = 0

# --- Heuristics ---
def get_h(tasks, completed, mode, c1, c2, limit_cg, limit_gm):
    remaining = [t for tid, t in tasks.items() if tid not in completed]
    if not remaining: return 0
    
    if mode == "min_days":
        # Admissible: Total prompts / max daily capacity
        total_p = sum(t.prompts for t in remaining)
        cap = (limit_cg + limit_gm) if (limit_cg + limit_gm) > 0 else 1
        return total_p / cap
    else:
        # Admissible: Actual cost of remaining tasks
        return sum(c1 if t.llm == "ChatGPT" else c2 for t in remaining)

# --- A* Algorithm ---
def solve_a_star(tasks, c1, c2, limit_cg, limit_gm, case, objective):
    global nodes_count
    nodes_count = 0
    # State: (cost/days, completed_set, current_day, day_prompts_cg, day_prompts_gm)
    start_h = get_h(tasks, set(), objective, c1, c2, limit_cg, limit_gm)
    pq = [(start_h, 0, set(), 1, 0, 0)] 
    visited = {}

    while pq:
        f, g, completed, day, p_cg, p_gm = heapq.heappop(pq)
        nodes_count += 1

        if len(completed) == len(tasks):
            return g if objective == "min_cost" else day, nodes_count

        state_key = (tuple(sorted(completed)), day, p_cg, p_gm)
        if state_key in visited and visited[state_key] <= g: continue
        visited[state_key] = g

        # Finding available tasks (predecessors done in PREVIOUS days)
        # Note: Assignment says "can share solution only on the next day"
        available = [t for tid, t in tasks.items() if tid not in completed 
                     and all(dep in completed for dep in t.deps)]

        # Option 1: Complete a task today
        for t in available:
            can_do = False
            if case == 'A' and p_cg == 0 and p_gm == 0: # Only 1 task per day
                can_do = True
            elif case == 'B': # Multiple tasks if prompts allow
                limit = limit_cg if t.llm == "ChatGPT" else limit_gm
                current_p = p_cg if t.llm == "ChatGPT" else p_gm
                if current_p + t.prompts <= limit:
                    can_do = True

            if can_do:
                new_completed = completed | {t.tid}
                cost_inc = c1 if t.llm == "ChatGPT" else c2
                new_p_cg = p_cg + (t.prompts if t.llm == "ChatGPT" else 0)
                new_p_gm = p_gm + (t.prompts if t.llm == "Gemini" else 0)
                
                # If Case A, must move to next day immediately after one task
                if case == 'A':
                    h = get_h(tasks, new_completed, objective, c1, c2, limit_cg, limit_gm)
                    heapq.heappush(pq, (g + cost_inc + h, g + cost_inc, new_completed, day + 1, 0, 0))
                else:
                    h = get_h(tasks, new_completed, objective, c1, c2, limit_cg, limit_gm)
                    heapq.heappush(pq, (g + cost_inc + h, g + cost_inc, new_completed, day, new_p_cg, new_p_gm))

        # Option 2: Move to next day (Wait)
        if p_cg > 0 or p_gm > 0: # Only if some work was done
            heapq.heappush(pq, (f, g, completed, day + 1, 0, 0))

    return None, nodes_count

# --- Main Execution ---
if __name__ == "__main__":
    if len(sys.argv) < 8:
        print("Usage: python assg03.py <input> <case: A/B> <obj: min_days/min_cost> <c1> <c2> <limit_cg> <limit_gm>")
        sys.exit(1)

    file = sys.argv[1]
    case = sys.argv[2]
    obj = sys.argv[3]
    try:
        c1 = int(sys.argv[4])
        c2 = int(sys.argv[5])
        l1 = int(sys.argv[6])
        l2 = int(sys.argv[7])
    except ValueError:
        print("Numeric arguments expected for c1, c2, limit_cg, limit_gm")
        sys.exit(1)
    tasks_data = parse_input(file)
    
    result, nodes = solve_a_star(tasks_data, c1, c2, l1, l2, case, obj)
    
    print("-" * 30)
    print(f"ALGORITHM: A* | CASE: {case} | OBJECTIVE: {obj}")
    print(f"Result (Value): {result}")
    print(f"Nodes Explored: {nodes}")
    print("-" * 30)