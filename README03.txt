ADVANCED ARTIFICIAL INTELLIGENCE LAB (CS5205)
                           Assignment 03

Problem Statement:

This assignment is a specialized extension of previous labs. We model a scenario 
where two different LLMs (ChatGPT and Gemini) are available to a group of students.
The goal is to solve optimization problems using advanced search algorithms.

KEY CONSTRAINTS:
   - LLM Allocation: Even-indexed assignments (A2, A4...) are solved by ChatGPT.
   - LLM Allocation: Odd-indexed assignments (A1, A3...) are solved by Gemini.
   - Costs: ChatGPT has cost c1 per prompt, and Gemini has cost c2 per prompt.
   - Subscription: Group-wise subscription limits (Total prompts per day for each LLM).

SCENARIOS:
   - Case-A: A student can perform only ONE assignment per day.
   - Case-B: A student can solve MULTIPLE assignments in a day if prompts are 
             available and dependencies are met.
   - Next-Day Rule: Solutions can only be shared on the next day at 6 AM.

PROBLEMS TO SOLVE:

1) Earliest Completion Time (Objective: min_days)
   Given a fixed subscription scheme (c1, c2 and daily limits), find the 
   minimum number of days to finish all tasks.

2) Best Subscription Plan (Objective: min_cost)
   Given a deadline of 'm' days, find the minimum total subscription cost 
   required to complete all tasks.

HOW TO RUN:

REQUIREMENTS:
   - Python 3.x

COMMAND STRUCTURE:
   python assg03.py <input_file> <case> <objective> <c1> <c2> <limit_cg> <limit_gm>

PARAMETERS:
   - <case>: 'A' or 'B'
   - <objective>: 'min_days' or 'min_cost'
   - <c1>, <c2>: Cost per prompt for ChatGPT and Gemini
   - <limit_cg>, <limit_gm>: Total daily prompts allowed for ChatGPT and Gemini

EXAMPLES:
   python assg03.py input01.txt B min_days 10 20 5 5
   python assg03.py input01.txt A min_cost 15 25 10 10

ALGORITHMS IMPLEMENTED:

1) A* Search (Primary):
   - Uses an admissible heuristic to find the optimal schedule.
   - Heuristic for min_days: h(n) = ceil(Remaining_Prompts / Total_Daily_Capacity)
   - Heuristic for min_cost: h(n) = Sum of costs of all remaining tasks.
   
2) Node Comparison Tracking:
   - The program tracks 'Nodes Explored' to evaluate the efficiency of the 
     search algorithm compared to standard DFS.

INPUT FORMAT:

Same as Assignment 01/02:
   A <Task_ID> <Prompt_Count> <Dependencies...> 0

OUTPUT FORMAT:

The program outputs a summary including:
   - Algorithm used (A*)
   - Case and Objective being solved
   - Optimal Value (Days or Cost)
   - Total Nodes Explored during search

---------------------------------------------------------------------------
Note: If no valid schedule exists within the constraints, the program will 
output "Infeasible" or "None".
---------------------------------------------------------------------------