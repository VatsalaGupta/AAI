                 Task Allocation & Scheduling System (LLM-based)
                           Assignment03

This project implements an intelligent scheduling system to allocate tasks between two LLMs (ChatGPT and Gemini) based on prompt costs,
daily limits, and task dependencies.

Features
- Objective 1: Find the earliest completion day and the total cost for a fixed subscription.
- Objective 2: Determine the cheapest subscription scheme to finish all tasks within `m` days.
- Search Algorithms:Implements DFS, Depth First Branch and Bound (DFBB), and A* Search.
- Constraint Handling:- Even-indexed tasks -> ChatGPT
    - Odd-indexed tasks -> Gemini
    - Case-A: Max 1 task per day.
    - Case-B: Multiple tasks per day (respecting limits and next-day dependency sharing).
How to Run
Ensure you have Python 3.6+ installed.

Command Format:
python assgn03.py <input_file> <cost_cg> <cost_gemini> <limit_cg> <limit_gemini> <max_days>

python assgn03.py input.txt 10 15 5 3 10

Thankyou!