╔════════════════════════════════════════════════════════════════════════════╗
║           📚 TASK ALLOCATION & SCHEDULING SYSTEM FOR STUDENTS 📚            ║
║                        Assignment Solver Program                            ║
╚════════════════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 WHAT'S THIS ALL ABOUT?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Imagine you have a group of N students who need to solve multiple assignments,
and each student has access to an LLM with a daily prompt limit. Here's the 
catch:

  📌 Each assignment needs a certain number of prompts to complete
  📌 Some assignments can ONLY be done after other assignments are done
  📌 Students can work on multiple tasks in a day (if they have prompts left)
  📌 A task CANNOT be split across multiple days
  📌 You have M days to finish everything

YOUR CHALLENGE: Find ALL the different ways to schedule these assignments
within M days while respecting everyone's constraints!

This program FINDS and COUNTS every valid schedule possible.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📖 QUICK START - HOW TO RUN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ REQUIREMENTS:
   • Python 3.x (any version 3.6 or newer)

✅ COMMAND:
   python assgn01.py <input_file> <number_of_days>

✅ EXAMPLES:
   python assgn01.py input01.txt 10
   python assgn01.py input02.txt 5
   python assgn01.py input03.txt 6

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📝 INPUT FILE FORMAT (How to Create Your Own)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The input file is simple and human-readable:

LINE 1:  % This is a comment (starts with %, gets ignored)
LINE 2:  N 3                    → 3 students in the group
LINE 3:  K 5                    → Each student can use 5 prompts per day
LINE 4+: A <id> <prompts> <deps> 0

Let's break down the Assignment line:
  • A          = This is an assignment line
  • <id>       = Name/ID of assignment (like "1", "2", "Task_A")
  • <prompts>  = How many prompts needed to solve it
  • <deps>     = Prerequisites (which assignments must be done first)
  • 0          = End marker (MUST be there!)

REAL EXAMPLE:
────────────────────────────────────────────────────────────────
% Example of assignment dependencies
N 2
K 5
A 1 2 0              → Assignment 1: needs 2 prompts, no dependencies
A 2 3 1 0            → Assignment 2: needs 3 prompts, depends on task 1
A 3 2 2 0            → Assignment 3: needs 2 prompts, depends on task 2
A 4 4 1 0            → Assignment 4: needs 4 prompts, depends on task 1
A 5 5 3 4 0          → Assignment 5: needs 5 prompts, depends on 3 AND 4
────────────────────────────────────────────────────────────────

🔗 WHAT DO DEPENDENCIES MEAN?
   → Task 2 can ONLY start after Task 1 is completed
   → Task 5 can only start after BOTH Task 3 and Task 4 are done

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 WHAT DOES THE OUTPUT LOOK LIKE?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

When you run the program, you'll see:

1️⃣  A SYSTEM STARTUP MESSAGE:
    ────────────────────────────────────────────────────────────
    TASK ALLOCATION SYSTEM
    ────────────────────────────────────────────────────────────
    >> Initializing solver for 10 assignments...
    >> Target Window: 6 days | Student Pool: 2
    >> Daily Quota per Student: 5 prompts
    >> Total Load: 27 units
    ────────────────────────────────────────────────────────────
    System is ready. DFS search...

2️⃣  VALID SCHEDULES (first 5 shown):
    >>> Valid Allocation #1 Found <<<
      Day 1: [Student1 handles 2], [Student2 handles 1]
      Day 2: [Student1 handles 3], [Student2 handles 4]
      Day 3: [Student1 handles 5], [Student2 handles 6]
      ...and so on

3️⃣  FINAL RESULTS:
    ────────────────────────────────────────────────────────────
    SOLVER FINISHED.
    Total distinct schedules discovered: 2560
    ────────────────────────────────────────────────────────────

💡 What does this mean?
   → We found 2,560 different valid ways to schedule these tasks!
   → Each way respects all dependencies and daily limits
   → The program shows you examples of the first 5 schedules

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧠 HOW DOES IT WORK? (Simple Explanation)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The program uses something called "BACKTRACKING":

Think of it like trying all possible routes on a maze:

  Day 1: "Which tasks CAN I do today?" 
         (Only the ones with no dependencies)
  
  Day 1: "I can do task 1. Should I assign it to student 1 or 2?"
         → Try BOTH options
         → Go to Day 2 with each option
  
  Day 2: "What's left to do? What can I do NOW?"
         → Check what tasks are ready
         → Try all ways to assign them
         → Go to Day 3
  
  ...and so on...
  
  SUCCESS: When all tasks are done within M days → Found a valid schedule!
  BACKTRACK: If we can't fit everything → Go back and try a different path

The program explores EVERY possible path and counts all valid schedules.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📁 SAMPLE INPUT FILES PROVIDED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Three different test cases are included:

1️⃣  input01.txt - LINEAR CHAIN
    → Tasks form a straight line: 1 → 2 → 3 → 4 → 5 → ... → 10
    → Each task depends on the previous one
    → Most restrictive (least flexibility in scheduling)
    
    TEST: python assgn01.py input01.txt 10
    RESULT: 1,024 valid schedules found

2️⃣  input02.txt - MULTIPLE INDEPENDENT PATHS
    → Tasks 1,2,3 have no dependencies (can start immediately)
    → Task 4 depends on 1 and 2
    → Task 5 depends on 1 and 3
    → Creates multiple branches
    
    TEST: python assgn01.py input02.txt 7
    RESULT: Many valid schedules (high flexibility)

3️⃣  input03.txt - MIXED DEPENDENCIES
    → Some tasks independent, some form chains, some have multiple deps
    → Moderate complexity
    
    TEST: python assgn01.py input03.txt 6
    RESULT: 2,560 valid schedules found

🔬 EACH FILE HAS AT LEAST 10 ASSIGNMENTS with DIFFERENT structures!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚙️ TECHNICAL DETAILS (For the Curious)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• Algorithm: Depth-First Search (DFS) with Backtracking
• Language: Python (compatible with all major OS)
• Time Complexity: Exponential (explores all possibilities)
• Space Complexity: O(M × N) where M = days, N = students
• Key Features:
  - Dependency tracking via sets
  - Daily quota management per student
  - All-or-nothing task assignment
  - Complete enumeration of valid schedules

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 IMPORTANT NOTES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ What the program DOES:
   • Finds ALL valid ways to schedule tasks
   • Respects task dependencies (prerequisites)
   • Respects student daily limits (prompts per day)
   • Counts total valid schedules
   • Shows examples of valid schedules

❌ What it DOES NOT do:
   • It can't split a task across multiple days
   • A student can't share remaining prompts with another student
   • Dependencies are STRICT (all must be met)

📌 Output Limit:
   • Program shows first 5 valid schedules (to keep output readable)
   • ALWAYS shows the TOTAL count of all valid schedules found

⏱️ Performance:
   • Larger problems take longer (more combinations to explore)
   • Linear chains (input01) run faster than mixed dependencies
   • Don't worry if it takes a few seconds - that's normal!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 WANT TO TEST IT?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Try these commands:

  # Linear chain - most restrictive
  python assgn01.py input01.txt 10

  # Mixed dependencies - moderate
  python assgn01.py input03.txt 6

  # Edge case - too few days
  python assgn01.py input01.txt 5     → Should find 0 schedules

  # Edge case - plenty of time
  python assgn01.py input03.txt 10    → Should find MORE schedules

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📧 ANY QUESTIONS?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This program is designed to be straightforward. If you're unsure:

1. Check the file format matches the examples above
2. Make sure Python 3.x is installed
3. Run with the exact command: python assgn01.py <file> <days>
4. Check error messages - they'll tell you what went wrong

The program will guide you if something's not right! ✨