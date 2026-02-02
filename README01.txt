            TASK ALLOCATION & SCHEDULING SYSTEM FOR STUDENTS           
                     Assignment 01                            

Problem Statement :

Imagine you have a group of N students who need to solve multiple assignments,
and each student has access to an LLM with a daily prompt limit.

   -Each assignment needs a certain number of prompts to complete
   -Some assignments can ONLY be done after other assignments are done
   -Students can work on multiple tasks in a day (if they have prompts left)
   -A task CANNOT be split across multiple days
   -You have M days to finish everything

We need to Find ALL the different ways to schedule these assignments
within M days while respecting everyone's constraints!

This program FINDS and COUNTS every valid schedule possible.

HOW TO RUN

REQUIREMENTS installation
   • Python 3.x (any version 3.6 or newer)

COMMAND:
   python assgn01.py <input_file> <number_of_days>

   EX:
   python assgn01.py input01.txt 10
   python assgn01.py input02.txt 5
   python assgn01.py input03.txt 6

 IMPORTANT NOTES :

 What the program DOES:
   • Finds ALL valid ways to schedule tasks
   • Respects task dependencies (prerequisites)
   • Respects student daily limits (prompts per day)
   • Counts total valid schedules
   • Shows examples of valid schedules

What it DOES NOT do:
   • It can't split a task across multiple days
   • A student can't share remaining prompts with another student
   • Dependencies are bit STRICT (all must be met)

 Output Limit:
   • Program shows first 5 valid schedules (to keep output readable)
   • AT Last it shows the TOTAL count of all valid schedules found

Performance:
   • Larger problems take longer time to explore
   • Linear chains (input01) run faster than mixed dependencies (input03)


  Run These commands for the output!!
  # For Linear chain - most restrictive
  python assgn01.py input01.txt 10

  # For Mixed dependencies - moderate
  python assgn01.py input03.txt 6

  # For Edge case - too few days
  python assgn01.py input01.txt 5     → IT Should find 0 schedules

  # For Edge case - plenty of time
  python assgn01.py input03.txt 10    → IT Should find MORE schedules

  Thankyou !!