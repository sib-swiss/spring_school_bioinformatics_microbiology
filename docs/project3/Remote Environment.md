# Setting in the remote environment


## General structure

Each student will get their own container for the duration of the course, where they can work, share and store data. 
This environment can be accessed with any internet browser, by going to your assigned port, which should look similar like http://1.23.45.678:10034.
In the container, you can find the following shared directories:

- /data: read only, and shared between all running containers. This directory is used to have a single place to store data
- /group_work: read and write enabled for all participants, and shared between all containers. This can be used to share data/scripts between students.
- ~/workdir: read and write enabled, and only shared between containers assigned to the same participant.
    
All directories other than the shared directories only exist within the container.

When visiting your assigned port, you should see the following window:

![](../assets/images/Project3/Fig1.png)

The features and parts you will mainly use are numbered. While going to the tabs (1) or (2) you can switch between our two interfaces: 
For our course, we will work mostly in the Terminal (Bash) for Part 1, and in the console (R) for Part2.

On the top right (3) is a panel in which you will be see which variables, dataframes etc. exist in your current session.

On the bottom right (4) you can see a visual representation of your directory structure, and you are also able to manually switch folders, create, delete and move files around. 



## Terminal

In order to use the preinstalled programms you will use during this course, it is first necessary to activate the conda environment in which they were installed.
To do this, go to the terminal tab and type 

```bash
conda activate project3
```
Afterwards, you should see (project3) on the left side, indicating that you are currently working within that environment. Now, you should be able to use the programms as described in their respective guides. For example, typing the following command should now print out the help section of fastqc.
```bash
fastqc -h 
```
If you need a quick refresher for the most common bash commands, for example to create directories, search for a specific word inside a file and similar tasks, check for example the following [guide.](https://www.educative.io/blog/bash-shell-command-cheat-sheet)



## Console

The console will be used mostly in Part2 of the course. Here, you have a set up R environment with all packages you will need preinstalled. 
You can create an R Script to better store and modify your code by selecting "R Script" in the icon below File.
+[](../assets/images/Project3/Fig2.png)



