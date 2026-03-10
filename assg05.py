import random
from itertools import combinations

class CourseScheduler:

    def __init__(self, room_count, course_list):
        self.room_count = room_count
        self.course_list = course_list
        self.var_ids = {}
        self.var_total = 0
        self.clauses = []

    # creating new SAT variable
    def get_var(self, key):
        if key not in self.var_ids:
            self.var_total += 1
            self.var_ids[key] = self.var_total
        return self.var_ids[key]

    def add(self, clause):
        self.clauses.append(clause)

    # -------- Encoding 1 --------
    # X(i,r,d) -> course i starts day d in room r

    def encode_v1(self):

        for i, (start, deadline, dur) in enumerate(self.course_list):

            days = range(start, deadline - dur + 2)
            choices = []

            for r in range(self.room_count):
                for d in days:
                    choices.append(self.get_var(("X", i, r, d)))

            self.add(choices)

            for a, b in combinations(choices, 2):
                self.add([-a, -b])

        self.room_overlap_rules()

    # avoiding overlapping of courses in same room
    def room_overlap_rules(self):

        n = len(self.course_list)

        for i in range(n):
            s1, d1, t1 = self.course_list[i]

            for j in range(i + 1, n):
                s2, d2, t2 = self.course_list[j]

                for r in range(self.room_count):

                    for d_i in range(s1, d1 - t1 + 2):
                        for d_j in range(s2, d2 - t2 + 2):

                            end_i = d_i + t1 - 1
                            end_j = d_j + t2 - 1

                            if not (end_i < d_j or end_j < d_i):

                                v1 = self.get_var(("X", i, r, d_i))
                                v2 = self.get_var(("X", j, r, d_j))

                                self.add([-v1, -v2])

    # -------- Encoding 2 --------
    # separating room and day variables

    def encode_v2(self):

        for i, (start, deadline, dur) in enumerate(self.course_list):

            days = range(start, deadline - dur + 2)

            room_vars = [self.get_var(("R", i, r)) for r in range(self.room_count)]
            day_vars = [self.get_var(("D", i, d)) for d in days]

            self.add(room_vars)
            self.add(day_vars)

            for a, b in combinations(room_vars, 2):
                self.add([-a, -b])

            for a, b in combinations(day_vars, 2):
                self.add([-a, -b])

        self.overlap_rules_v2()

    def overlap_rules_v2(self):

        n = len(self.course_list)

        for i in range(n):
            s1, d1, t1 = self.course_list[i]

            for j in range(i + 1, n):
                s2, d2, t2 = self.course_list[j]

                for r in range(self.room_count):

                    for d_i in range(s1, d1 - t1 + 2):
                        for d_j in range(s2, d2 - t2 + 2):

                            end_i = d_i + t1 - 1
                            end_j = d_j + t2 - 1

                            if not (end_i < d_j or end_j < d_i):

                                r1 = self.get_var(("R", i, r))
                                r2 = self.get_var(("R", j, r))

                                d1v = self.get_var(("D", i, d_i))
                                d2v = self.get_var(("D", j, d_j))

                                self.add([-r1, -r2, -d1v, -d2v])

    # DIMACS file
    def save_cnf(self, name):

        with open(name, "w") as f:

            f.write(f"p cnf {self.var_total} {len(self.clauses)}\n")

            for c in self.clauses:
                f.write(" ".join(map(str, c)) + " 0\n")


# -------- Random testcase generator --------

def make_random_data():

    rooms = random.randint(2, 5)
    n = random.randint(5, 10)

    courses = []

    for _ in range(n):

        start = random.randint(1, 10)
        length = random.randint(1, 4)
        deadline = start + random.randint(length, 6)

        courses.append((start, deadline, length))

    return rooms, courses


# -------- main --------

if __name__ == "__main__":

    rooms, courses = make_random_data()
    
    print("Number of rooms:", rooms)
    print("Number of courses:", len(courses))

    for i, c in enumerate(courses):
     print(f"Course {i} -> start:{c[0]} deadline:{c[1]} duration:{c[2]}")

    s1 = CourseScheduler(rooms, courses)
    s1.encode_v1()
    s1.save_cnf("encoding1.cnf")

    s2 = CourseScheduler(rooms, courses)
    s2.encode_v2()
    s2.save_cnf("encoding2.cnf")

    print("CNF files created.")