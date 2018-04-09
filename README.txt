There are 3 .py files and 1 .txt file:

1. gui_obj.py: the main Python file for the GUI.
2. reading_files.py: the Python script used to generate snap graphs from PostgreSQL databases.
3. util.py: File containing methods to generate characteristics. 

1


To run the main program:

Pre-requisite:
1. Place the four files in one directory
2. Install these dependencies to your Python: snap, numpy, matplotlib, gnuplot, psycopg2, Tkinter

Running the program:
1. Open command prompt
2. Change directory to the directory of the four files
3. python gui_obj.py

Note that the program may take a while to load as it loads the TPC-H Benchmark graph & generate random and scale-free graphs

4. Choose a graph to load
	4.1 Load a PostgreSQL network
	4.2 Load a Snap network
	4.3 Generate a random network 
	4.4 generate a scale-free network

5. Click on the properties you want to generate
6. The program will show the graphs generated

Careful:
1. You need to enter the right credentials for the PostgreSQL network.
2. The Snap file needs to be an edge list.
3, Manually delete all the PNG graphs generated before you load a new graph (Not obligatory)
4. Close all the unexpected pop-up windows



