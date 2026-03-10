import itertools
import random
import os

class Course:
    def __init__(self, cid, start, end, duration):
        self.cid = cid
        self.start = start
        self.end = end
        self.duration = duration

class SATScheduler:
    def __init__(self, rooms, courses):
        self.rooms = rooms
        self.courses = courses
        self.variables = {}
        self.var_count = 0
        self.clauses = []

    def get_var(self, key):
        if key not in self.variables:
            self.var_count += 1
            self.variables[key] = self.var_count
        return self.variables[key]

    def add_clause(self, clause):
        self.clauses.append(clause)

    def print_stats(self, encoding_name):
        c2 = sum(1 for c in self.clauses if len(c) == 2)
        c3 = sum(1 for c in self.clauses if len(c) == 3)
        c4plus = sum(1 for c in self.clauses if len(c) >= 4)
        
        print(f"Encoding: {encoding_name}")
        print(f"Variables: {self.var_count}")
        print(f"Clauses: {len(self.clauses)}")
        print(f"2-literal clauses: {c2}")
        print(f"3-literal clauses: {c3}")
        print(f"4+-literal clauses: {c4plus}")

    def encode_option1(self):
        self.variables, self.var_count, self.clauses = {}, 0, []
        for c in self.courses:
            possible = []
            for t in range(c.start, c.end - c.duration + 2):
                for r in range(1, self.rooms + 1):
                    v = self.get_var((c.cid, t, r))
                    possible.append(v)
            self.add_clause(possible)
            for a, b in itertools.combinations(possible, 2):
                self.add_clause([-a, -b])

        for c1, c2 in itertools.combinations(self.courses, 2):
            for r in range(1, self.rooms + 1):
                for t1 in range(c1.start, c1.end - c1.duration + 2):
                    for t2 in range(c2.start, c2.end - c2.duration + 2):
                        if not (t1 + c1.duration - 1 < t2 or t2 + c2.duration - 1 < t1):
                            v1 = self.get_var((c1.cid, t1, r))
                            v2 = self.get_var((c2.cid, t2, r))
                            self.add_clause([-v1, -v2])

    def encode_option2(self):
        self.variables, self.var_count, self.clauses = {}, 0, []
        for c in self.courses:
            room_vars = [self.get_var(("room", c.cid, r)) for r in range(1, self.rooms + 1)]
            time_vars = [self.get_var(("time", c.cid, t)) for t in range(c.start, c.end - c.duration + 2)]
            self.add_clause(room_vars)
            for a, b in itertools.combinations(room_vars, 2): self.add_clause([-a, -b])
            self.add_clause(time_vars)
            for a, b in itertools.combinations(time_vars, 2): self.add_clause([-a, -b])

        for c1, c2 in itertools.combinations(self.courses, 2):
            for r in range(1, self.rooms + 1):
                y1, y2 = self.get_var(("room", c1.cid, r)), self.get_var(("room", c2.cid, r))
                for t1 in range(c1.start, c1.end - c1.duration + 2):
                    for t2 in range(c2.start, c2.end - c2.duration + 2):
                        if not (t1 + c1.duration - 1 < t2 or t2 + c2.duration - 1 < t1):
                            z1, z2 = self.get_var(("time", c1.cid, t1)), self.get_var(("time", c2.cid, t2))
                            self.add_clause([-y1, -z1, -y2, -z2])

    def write_dimacs(self, file):
        with open(file, "w") as f:
            f.write(f"p cnf {self.var_count} {len(self.clauses)}\n")
            for c in self.clauses:
                f.write(" ".join(map(str, c)) + " 0\n")

def read_input(filename):
    with open(filename) as f:
        lines = f.readlines()
    rooms = int(lines[0])
    n = int(lines[1])
    courses = []
    for i in range(n):
        parts = lines[i+2].split()
        courses.append(Course(int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3])))
    return rooms, courses

def generate_100_cases():
    for i in range(100):
        rooms = random.randint(2, 6)
        n = random.randint(5, 15)
        with open(f"test{i}.txt", "w") as f:
            f.write(f"{rooms}\n{n}\n")
            for cid in range(1, n + 1):
                start = random.randint(1, 20)
                dur = random.randint(1, 5)
                end = start + random.randint(dur, 10)
                f.write(f"{cid} {start} {end} {dur}\n")

if __name__ == "__main__":
    generate_100_cases()
    print("100 test cases generated.")


    rooms, courses = read_input("test0.txt")
    solver = SATScheduler(rooms, courses)

    print("\n--- Sample Output for test0.txt ---")
    solver.encode_option2()
    solver.print_stats("option2")
    solver.write_dimacs("output2.cnf")

    print("-" * 25)

    solver.encode_option1()
    solver.print_stats("option1")
    solver.write_dimacs("output1.cnf")