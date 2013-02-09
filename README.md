The main goal of this function is alter the user when a large
 program has finished running.

It has three time-based functions. This lets the user know
when the function began, and how long it took.

It has two messaging functions.
  The first takes an error title, and sends a message to the
  user altering her/him of the error

  The second takes a start and end time, and a name of the
  function that takes a large amount of time for my reference 
  and convenience. This function is called when the large
  program is completed, and sends the message to the user. 


The way I use this setup is as follows
  I traditionally have a main() function
  The main() will execute all of the functions of my major
  program. At the top of the main() I call get_time()
  which, non-surprisingly returns the time. I store it in
  some variable start_time. I also usually call
  show_Full_Time() that way at the top of the output for
  whatever program I'm running, I have the start time.
  After the program completes, and I'm at the end of main()
  I call doneTextSend(start_Time, get_time(), process_Name)
  where process_Name is a string for my reference later on.
