import sys
import heapq

class TaskDetail:
    def __init__(self, label, cost, dependency_list):
        self.label = label
        self.cost = cost
        self.dependencies = set(dependency_list)

class Schedule_Optimizer:
    def __init__(self, number_Of_students, capacity_per_day, horizon, task_map):
        self.student_count = number_Of_students
        self.daily_limit = capacity_per_day
        self.total_days = horizon
        self.all_tasks = task_map
      
        self.remaining_budget = {
            i: [capacity_per_day] * horizon for i in range(1, number_Of_students + 1)
        }
        
        self.assignments = []
        self.done_tasks = set()
        self.solutions_found = 0
        self.visited_states = set()

    def generating_state_key(self):
        tasks_snapshot = tuple(sorted(list(self.done_tasks)))
        budget_snapshot = tuple(tuple(self.remaining_budget[s]) for s in range(1, self.student_count + 1))
        return (tasks_snapshot, budget_snapshot)

    def finding_executable_tasks(self):
        ready = []
        for tid, t_obj in self.all_tasks.items():
            if tid not in self.done_tasks:
                if t_obj.dependencies.issubset(self.done_tasks):
                    ready.append(tid)
        ready.sort() 
        return ready

    def executing_search(self):
        if len(self.done_tasks) == len(self.all_tasks):
            self.displaying_the_result()
            return True

        present_state = self.generating_state_key()
        if present_state in self.visited_states:
            return False
        self.visited_states.add(present_state)

        available = self.finding_executable_tasks()
        if not available:
            return False

        target_task = available[0]
        task_info = self.all_tasks[target_task]

        for s_idx in range(1, self.student_count + 1):
            for d_idx in range(self.total_days):
                if self.remaining_budget[s_idx][d_idx] >= task_info.cost:
                
                    self.remaining_budget[s_idx][d_idx] -= task_info.cost
                    self.done_tasks.add(target_task)
                    self.assignments.append((target_task, s_idx, d_idx))

                    self.executing_search()
                    self.assignments.pop()
                    self.done_tasks.remove(target_task)
                    self.remaining_budget[s_idx][d_idx] += task_info.cost
        
        return self.solutions_found > 0

    def displaying_the_result(self):
        self.solutions_found += 1
        if self.solutions_found > 5: return
        
        print(f"\n Alternative Schedule Plan {self.solutions_found} ---")
        output = {}
        for tid, sid, day in self.assignments:
            if sid not in output: output[sid] = {}
            if day not in output[sid]: output[sid][day] = []
            output[sid][day].append(tid)

        for s in sorted(output.keys()):
            print(f"Student {s}:")
            for d in sorted(output[s].keys()):
                print(f"  Day {d+1}: {', '.join(output[s][d])}")

def run_engine():
    if len(sys.argv) < 3:
        print("Error: Missing arguments (input_file, max_days)")
        return

    raw_tasks = {}
    try:
        with open(sys.argv[1], 'r') as source:
            for line in source:
                bits = line.strip().split()
                if not bits or bits[0].startswith('%'): continue
                
                header = bits[0]
                if header == 'N': n_val = int(bits[1])
                elif header == 'K': k_val = int(bits[1])
                elif header == 'A':
                    name = bits[1]
                    weight = int(bits[2])
                    deps = [d for d in bits[3:] if d != '0']
                    raw_tasks[name] = TaskDetail(name, weight, deps)
    except Exception as e:
        print(f"File Error: {e}")
        return

    window = int(sys.argv[2])
    engine = Schedule_Optimizer(n_val, k_val, window, raw_tasks)

    print("Initializing Search Engine...")
    engine.executing_search()
    print(f"\nSearch concluded. Found {engine.solutions_found} valid configurations.")

if __name__ == "__main__":
    run_engine()