# Lesson 7 Assignment

The code for this assignment will be somewhat familiar to you, because we are
 building
 on our work from week 6. However, this time we are focusing on
  understanding and improving performance by introducing parallel processing
  . We will not be using Alice's memoize function!

The scenario is the same: The calc program is performing poorly. Ever since it was implemented it has taken a long time to run.

The program as it stands has been partially reworked to assess the
 benefit of using Pools.
Your job is to understand the runtime characteristics of the program "as
 is", and then implement two other alternatives to Pools, following the same
  pattern as Pools. This is so you can see and understand the performance
   potential of the various approaches (serial, pools, and then the two you chose). Also, you need to find a way
    to speed up writing the csv files, which now write a total of around
     10Gb when done.

Thus, like last week, you will need to use an evidence-based approach, using timing, profiling, and any other tools you may need. You will need  to document this as you go, and submit this documentation with your assignment. 

All code is in lesson07_assignment in this repo.

## What you must do
1. Understand the multi.py program by reading and running it.
1. Answer the following preliminary questions (the answers must be included
 with your
 submission):
    - explain the time difference between the serial and parallel functions
    - explain why serial is faster in the first number_set and slower in
     the rest
    - What is the impact of changing Pool(size) to different values? Why? Does it even make a difference? Why?

1. Then, write two more functions, like parallel, and following it's pattern
, that use other ways to attempt the work in parallel. Answer the questions
 in 2 above, but comparing serial and parallel to your two new functions.
1. Add a function that attempt to write the csv files in parallel. Compare
 your parallel approach to the save_serial approach. There is a function
  stub to help with printing. Note that the files must include the header and footer, like in save_serial.
  
# Your submission
All code should score at least 9/10 when linted. Include tests if you wish
. Provide a document that describes the before and after performance as
 described above for all your work.

