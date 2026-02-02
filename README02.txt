            TASK ALLOCATION & SCHEDULING SYSTEM FOR STUDENTS           
                            Assignment 02                            

Problem Statement :

This assignment is an extension of Assignment 01.

We schedule assignment tasks for a group of students who use an LLM with
a limited number of prompts per day. In addition to task dependencies and
daily prompt limits, we now solve optimization problems and introduce a
realistic solution-sharing delay rule.

IMPORTANT CHANGE FROM ASSIGNMENT 01:
   - The group size (N) and prompt count (K) in the input file are IGNORED
   - These values are taken ONLY from the command line

PROBLEMS TO SOLVE:

1) Earliest Completion Time

   Given:
      • Group size (N students)
      • Prompts per student per day (K)

   We find the MINIMUM number of days required to complete all assignments
   while respecting:
      • Task dependencies
      • Daily prompt limits

2) Minimum Subscription Plan

   Given:
      -Group size (N students)
      -Deadline (number of days)

   We find the MINIMUM prompts per student per day (K) required so that
   all assignments can be completed within the given days.


3) NEXT-DAY SOLUTION SHARING RULE (6 AM Rule)

   In this scenario:

   -Students start solving tasks each day at 6 AM
   -Solutions of completed tasks are shared ONLY at 6 AM the NEXT day
   -A task can start only if:
        - Student has enough prompts that day
        - ALL dependencies finished on a Previous day

   So dependency rule becomes:
        Dependency_Finish_Day < Current_Day

   Under this rule, we again solve:
        -Earliest completion time
        -Minimum subscription plan

HOW TO RUN

REQUIREMENTS installation
   • Python 3.x (any version 3.6 or newer)

COMMAND:
   python assg02.py <input_file> <max_days> <N> <K> [--nextday]

EXAMPLES:

   python assg02.py input01.txt 10 2 5
   python assg02.py input02.txt 8 3 4
   python assg02.py input01.txt 10 2 5 --nextday

   (Use --nextday to enable the 6 AM sharing rule — required for Part 3)

INPUT FORMAT

Same as Assignment 01 for tasks:

   A <Task_ID> <Cost> <Dependencies...> 0

Each line in input:
A TaskID Cost Dependency1 Dependency2 ... 0

IMPORTANT:
   - N and K values written in the file are IGNORED
   - Only command-line N and K are used

OUTPUT FORMAT

The program prints:
• For Problem 1 → Minimum days required
• For Problem 2 → Minimum prompts per student per day (K)
• If --nextday is used → Results under next-day sharing rule

ALGORITHM USED

- Backtracking Search assigns tasks to (Student, Day) slots
- Daily prompt limits are strictly enforced
- Task dependencies must be satisfied before scheduling

For Problem 1:
   - Linear search on number of days

For Problem 2:
   - Binary Search on K (minimum prompts per day)

For Problem 3:
   - Dependency check modified to enforce next-day availability

Thankyou !!
