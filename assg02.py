import sys
from copy import deepcopy

class Task_Detail:
    def __init__(self, labeling, price , dependencylist):
        self.labeling = labeling
        self.price = price
        self.dependencies = set(dependencylist)

def loading_tasks(file):
    tasks = {}
    with open(file) as f:
        for line in f:
            parts = line.strip().split()
            if not parts or parts[0].startswith('%'):
                continue
            if parts[0] == 'A':
                tid = parts[1]
                price = int(parts[2])
                deps = [x for x in parts[3:] if x != '0']
                tasks[tid] = Task_Detail(tid, price, deps)
    return tasks

class Schedule_Optimizer:
    def __init__(self, N, K, days, tasks, nextday=False):
        self.N = N                      
        self.K = K                     
        self.days = days
        self.tasks = tasks
        self.nextday = nextday

        self.remaining = {s: [K]*days for s in range(N)}
        self.done = set()
        self.finish_day = {}          
        self.memo = set()
        
    def state_key(self):
        return (tuple(sorted(self.done)),
                tuple(tuple(self.remaining[s]) for s in range(self.N)))
        
    def available_tasks(self, day):
        ready = []
        for t in self.tasks:
            if t not in self.done and self.deps_satisfied(t, day):
                ready.append(t)
        return sorted(ready)
    

    def deps_satisfied(self, task, day):
        for dep in self.tasks[task].dependencies:
            if dep not in self.done:
                return False
            if self.nextday:
                if self.finish_day[dep] >= day:
                    return False
        return True


    def search(self):
        if len(self.done) == len(self.tasks):
            return True

        key = self.state_key()
        if key in self.memo:
            return False
        self.memo.add(key)

        for day in range(self.days):
            tasks_today = self.available_tasks(day)
            for task in tasks_today:
                price = self.tasks[task].price

                for s in range(self.N):
                    if self.remaining[s][day] >= price:

                        self.remaining[s][day] -= price
                        self.done.add(task)
                        self.finish_day[task] = day

                        if self.search():
                            return True

                        self.remaining[s][day] += price
                        self.done.remove(task)
                        del self.finish_day[task]
        return False

def earliest_completion(tasks, N, K, nextday):
    for day in range(1, 50): 
        engine = Schedule_Optimizer(N, K, day, tasks, nextday)
        if engine.search():
            return day
    return -1

def minimum_subscription(tasks, N, deadline, nextday):
    low, high = 1, 50
    result = -1

    while low <= high:
        mid_value = (low + high) // 2
        engine = Schedule_Optimizer(N, mid_value, deadline, tasks, nextday)

        if engine.search():
            ans = mid_value
            high = mid_value - 1
        else:
            low = mid_value + 1
    return result

def main():
    if len(sys.argv) < 5:
        print("Usage: python assg02.py <input_file> <max_days> <N> <K> [--nextday]")
        return

    file = sys.argv[1]
    maximum_days = int(sys.argv[2])
    N = int(sys.argv[3])
    K = int(sys.argv[4])
    next_day = '--nextday' in sys.argv

    tasks = loading_tasks(file)

    print("\n--- PROBLEM 1: Earliest Completion Time ---")
    days = earliest_completion(tasks, N, K, next_day)
    print(f"Minimum days required = {days}")

    print("\n--- PROBLEM 2: Minimum Subscription Plan ---")
    k_needed = minimum_subscription(tasks, N, maximum_days, next_day)
    print(f" SO , Minimum prompts per student per day = {k_needed}")

    if next_day:
        print("\n(Results computed under NEXT_DAY 6 AM SHARING RULE)")

if __name__ == "__main__":
    main()
