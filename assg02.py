import sys

class TaskDetail:
    def __init__(self, label, cost, dependency_list):
        self.label = label
        self.cost = cost
        self.dependencies = set(dependency_list)

class Schedule_Optimizer:
    def __init__(self, student_count, capacity_per_day, horizon, task_map, next_day_rule=False):
        self.student_count = student_count
        self.daily_limit = capacity_per_day
        self.total_days = horizon
        self.all_tasks = task_map
        self.next_day_rule = next_day_rule
        
        # Tracking resources and state
        self.remaining_budget = {i: [capacity_per_day] * horizon for i in range(1, student_count + 1)}
        self.completion_days = {} 
        self.done_tasks = set()
        self.assignments = []

    def can_schedule(self, task_id, day):
        task = self.all_tasks[task_id]
        for dep in task.dependencies:
            if dep not in self.done_tasks:
                return False
            # Constraint: Solution available only at 6am the next day
            if self.next_day_rule and self.completion_days[dep] >= day:
                return False
        return True

    def solve(self):
        if len(self.done_tasks) == len(self.all_tasks):
            return True

        # Find tasks whose dependencies are met
        available = [tid for tid in self.all_tasks if tid not in self.done_tasks and self.can_schedule(tid, self.total_days)]
        if not available: return False
        
        target_task = sorted(available)[0]
        task_info = self.all_tasks[target_task]

        for day in range(self.total_days):
            if not self.can_schedule(target_task, day): continue
            
            for s_idx in range(1, self.student_count + 1):
                if self.remaining_budget[s_idx][day] >= task_info.cost:
                    # Apply Assignment
                    self.remaining_budget[s_idx][day] -= task_info.cost
                    self.done_tasks.add(target_task)
                    self.completion_days[target_task] = day
                    self.assignments.append((target_task, s_idx, day))

                    if self.solve(): return True

                    # Backtrack
                    self.assignments.pop()
                    del self.completion_days[target_task]
                    self.done_tasks.remove(target_task)
                    self.remaining_budget[s_idx][day] += task_info.cost
        return False

    def format_schedule(self):
        """Return a formatted string representing the schedule.
        The schedule is grouped by day and shows which student worked on which tasks."""
        out_lines = []
        # Build mapping day -> student -> list(tasks)
        day_map = {d: {s: [] for s in range(1, self.student_count + 1)} for d in range(self.total_days)}
        for (t, s, d) in self.assignments:
            if d in day_map and s in day_map[d]:
                day_map[d][s].append(t)
        for d in range(self.total_days):
            out_lines.append(f"Day {d+1}:")
            any_work = False
            for s in range(1, self.student_count + 1):
                tasks = day_map[d][s]
                if tasks:
                    any_work = True
                    out_lines.append(f"  Student {s}: {', '.join(tasks)}")
            if not any_work:
                out_lines.append("  No assignments scheduled")
        return "\n".join(out_lines)

    def print_schedule(self):
        print(self.format_schedule())

def run_assignment():
    # Usage: python assg02.py <input_file> <max_days> [N K] [--nextday]
    if len(sys.argv) < 3:
        print("Usage: python assg02.py <input_file> <max_days> [N K] [--nextday]")
        return

    input_file = sys.argv[1]
    max_days_allowed = int(sys.argv[2])
    # Group size (N) and prompts per student (K) must be provided on the command line
    cmd_N = None
    cmd_K = None
    next_day_mode = False
    print_schedule = False
    # parse remaining args (order-insensitive): expect two integers and flags
    tail = sys.argv[3:]
    remaining_ints = []
    for t in tail:
        if t == '--nextday':
            next_day_mode = True
        elif t in ('--print-schedule', '--verbose'):
            print_schedule = True
        else:
            # collect integer-looking tokens as N and K
            try:
                remaining_ints.append(int(t))
            except:
                pass
    if len(remaining_ints) >= 2:
        cmd_N, cmd_K = remaining_ints[0], remaining_ints[1]
    else:
        print("Error: This assignment requires N (group size) and K (prompts per student per day) to be provided on the command line.")
        print("Usage: python assg02.py <input_file> <max_days> N K [--nextday] [--print-schedule|--verbose]")
        return
    
    raw_tasks = {}
    n_val, k_val = 0, 0

    # Robust File Parsing
    try:
        with open(input_file, 'r') as source:
            for line in source:
                bits = line.strip().split()
                if not bits or bits[0].startswith('%'): continue
                if bits[0] == 'N': n_val = int(bits[1])
                elif bits[0] == 'K': k_val = int(bits[1])
                elif bits[0] == 'A':
                    name, weight = bits[1], int(bits[2])
                    deps = [d for d in bits[3:] if d != '0']
                    raw_tasks[name] = TaskDetail(name, weight, deps)
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Problem 1: Earliest Completion Time
    print(f"\n--- Problem 1: Earliest Time (NextDay Mode: {next_day_mode}) ---")
    earliest = -1
    earliest_solver = None
    for d in range(1, max_days_allowed + 1):
        # allow command-line overrides of N and K
        use_n = cmd_N if cmd_N is not None else n_val
        use_k = cmd_K if cmd_K is not None else k_val
        solver = Schedule_Optimizer(use_n, use_k, d, raw_tasks, next_day_mode)
        if solver.solve():
            earliest = d
            earliest_solver = solver
            break
    print(f"Result: {earliest if earliest != -1 else 'No valid schedule'} days")
    if print_schedule and earliest_solver is not None:
        print("\n--- Schedule for earliest completion ---")
        earliest_solver.print_schedule()

    # Problem 2: Minimum Subscription Scheme
    print(f"\n--- Problem 2: Minimum Prompts (K) for {max_days_allowed} Days ---")
    low, high = 1, sum(t.cost for t in raw_tasks.values())
    min_k = high
    found_any = False
    best_solver = None
    while low <= high:
        mid = (low + high) // 2
        use_n = cmd_N if cmd_N is not None else n_val
        solver = Schedule_Optimizer(use_n, mid, max_days_allowed, raw_tasks, next_day_mode)
        if solver.solve():
            min_k, found_any = mid, True
            best_solver = solver
            high = mid - 1
        else:
            low = mid + 1
    print(f"Result: {min_k if found_any else 'Impossible'} prompts/day")
    if print_schedule and found_any and best_solver is not None:
        print("\n--- Schedule for minimum prompts/day scheme ---")
        best_solver.print_schedule()

if __name__ == "__main__":
    run_assignment()