# deadline-watchdog
 A Deadline Watchdog that manages farm priorities etc

## Aim & use case
A watchdog script that can periodically scan the Deadline farm for queued/rendering/pending jobs and adjust those automatically based on preset filters.

For example, production wants to give all renders of shot AA_TST_0015 priority for today as it needs to go out to the client.
A filter can be added to the watchdog to scan for all jobs containing that shotname in the job name and adjust it's settings automatically.
In this case, we could add a filter for "aa_tst_0015" (watchdog is case insensitive), set the pool to "high" and the priority to "80".

## Installation
Download a release from github, unzip and place the folder somewhere on your local or shared storage (preffered) and run the deadline-watchdog.py to display the GUI interface and add filters.

## Usage
The watchdog can run unattended using the -run argument. 
Filters will have to be added using the GUI but this can be done from a different computer, as long as you load from the same installation folder.

The menu will display the following options:

### 1 - Start watchdog...
Starts the watchdog in GUI mode running on the current computer.

### 2 - Add jobfilter
Add a jobfilter, for example "tst_0050" will scan for all jobs with this in the name.
Set a pool and priority to adjust matching jobs to.

### 3 - Remove jobfilter
Not implemented yet...

### 4 - View jobfilters
Displays all jobfilters currently in the jobfilters file.

### 5 - Reset all jobfilters
Resets all jobfilters.

### 6 - Send Deadline Watchdog Job to farm...
Sends a suspended Python Deadline job to the farm which runs the watchdog in command line mode

