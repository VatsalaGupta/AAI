import sys

# Global variables to match your professional C++ structure
total_N = 0
daily_K = 0
max_M = 0
taskDict = {}
allTaskNames = []
currentSchedule = []
validCount = 0

class Assignment:
    def __init__(self, name, weight, preReqs):
        self.name = name
        self.weight = weight
        self.preReqs = preReqs

def showInitialReport():
    totalLoad = sum(t.weight for t in taskDict.values())
    print("-" * 60)
    print("    TASK ALLOCATION SYSTEM")
    print("-" * 60)
    print(f">> Initializing solver for {len(allTaskNames)} assignments...")
    print(f">> Target Window: {max_M} days | Student Pool: {total_N}")
    print(f">> Daily Quota per Student: {daily_K} prompts")
    print(f">> Total Load: {totalLoad} units")
    print("-" * 60)
    print("System is ready. DFS search...")
    print("-" * 60 + "\n")

def recordValidPath():
    global validCount
    validCount += 1
    # Limiting to 5 to keep terminal clean as per your C++ logic
    if validCount <= 5:
        print(f">>> Valid Allocation #{validCount} Found <<<")
        for d, day_tasks in enumerate(currentSchedule):
            if not day_tasks: continue
            # Format: [Student1 handles A1], [Student2 handles A2]
            work_details = ", ".join([f"[Student{s} handles {t}]" for s, t in day_tasks])
            print(f"  Day {d + 1}: {work_details}")
        print()

def runEngine(idx, d, done, readyList, quotas, work):
    global currentSchedule
    
    if idx == len(readyList):
        # Move to next day with the accumulated work
        currentSchedule.append(list(work))
        nextDone = done.union({w[1] for w in work})
        backtrackSolver(d + 1, nextDone)
        currentSchedule.pop()
        return

    task_id = readyList[idx]
    weight = taskDict[task_id].weight

    # Path 1: Skip this task for now (try it on a later day)
    runEngine(idx + 1, d, done, readyList, quotas, work)

    # Path 2: Assign to a student with capacity
    for s in range(1, total_N + 1):
        if quotas[s] >= weight:
            quotas[s] -= weight
            work.append((s, task_id))
            runEngine(idx + 1, d, done, readyList, quotas, work)
            work.pop()
            quotas[s] += weight

def backtrackSolver(currentDay, finished):
    global currentSchedule
    
    if len(finished) == len(taskDict):
        recordValidPath()
        return
    if currentDay >= max_M:
        return

    # Check for ready tasks
    canStart = [id for id in allTaskNames if id not in finished and all(p in finished for p in taskDict[id].preReqs)]

    # If no tasks are ready but time remains, try skipping a day
    if not canStart:
        if currentDay < max_M:
            currentSchedule.append([])
            backtrackSolver(currentDay + 1, finished)
            currentSchedule.pop()
        return

    # Create quota array for this day
    quotas = [0] + [daily_K] * total_N  # Index 0 unused, 1 to total_N for students
    runEngine(0, currentDay, finished, canStart, quotas, [])

def main():
    global total_N, daily_K, max_M, allTaskNames, taskDict
    if len(sys.argv) < 3:
        print("Incorrect usage. Try: python assgn01.py <input_file> <m_days>")
        return

    # Parsing input file
    with open(sys.argv[1], 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('%'): continue
            parts = line.split()
            if parts[0] == 'N': 
                total_N = int(parts[1])
            elif parts[0] == 'K': 
                daily_K = int(parts[1])
            elif parts[0] == 'A':
                t_id = parts[1]
                # Format: A <id> <weight> <dep1> <dep2> ... <0>
                # Filter out '0' terminating symbol from dependencies
                deps = [d for d in parts[3:] if d != '0']
                taskDict[t_id] = Assignment(t_id, int(parts[2]), deps)
                allTaskNames.append(t_id)
    
    max_M = int(sys.argv[2])
    showInitialReport()
    backtrackSolver(0, set())
    
    print("-" * 60)
    print("SOLVER FINISHED.")
    print(f"Total distinct schedules discovered: {validCount}")
    print("-" * 60)

if __name__ == "__main__":
    main()