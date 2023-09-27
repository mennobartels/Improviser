# Improvisor
A path improvisor using ApproxMC and Z3. Created for my research internship

# Description
This repository contains the files for an improvisor that finds a path using the approximate model counter ApproxMC. 
In the file Example.py a basic usage can be found. 

The Improvisor class has the following arguments

csv -- the input file as a csv
steps -- the amount of steps the improvisor may take
lam -- the lambda used, 0 if uninitialized 
eps -- epsilon used, 0.8 if uninitialized
show -- boolean for printing out intermediate results, False if uninitialized

Some remarks:
The csv file has the following format:
0 is an open square
S is the start square
F is the finishing square
W is a wall/obstacle
Note that S and F can only occur once



# Usage 
When cloning the repository, there are two main ways to use the code:

Docker:
Build the image with 
docker build -t improviser-image

Run a container with 
docker run -it -rm improvisor-image /bin/bash

This gives an interactive session within the container that is running. Then an example can be ran with
python Example.py

This example can be altered by using nano which is installed in the container. Also nano can be used to alter the grid for the example. Note that if the grid changes, the input for the amoutn of steps and lambda would have to change. 

When running the container, the animations will nog be available as the container only gives a command line. 

Local:
To run the files locally it is advised to start up a venv and install the rights packages with the requirements.txt file. Then the Example.py file can be ran in the venv as normal. 

Locally the Example_with_animation.py file will also work, and will save animations as mp4's.
