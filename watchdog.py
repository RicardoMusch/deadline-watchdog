app_name = "Deadline Watchdog"
version = "dev"

import os
from os import system
import sys
import socket
import deadline_utils
import time

# Start app
os.system("cls")

print("Getting Deadline configuration...")
pools = deadline_utils.get_pools()


def main():
    "Main app run"
    _ensure_jobfilters_exist()
    menu()

def menu():
    "Menu with choices"

    _header()
    print("Choose your option:")
    _dashingLine()
    print("1 - Add jobfilter")
    print("2 - Remove jobfilter")
    print("3 - View jobfilters")
    print("4 - Reset all jobfilters")
    print("5 - Start watchdog...")

    print(" ")
    print("Make your choice:")
    choice = raw_input("")


    if choice.strip("") == "1":
        add_jobfilter()
    elif choice.strip("") == "2":
        remove_jobfilter()
    elif choice.strip("") == "3":
        view_jobfilters()
    elif choice.strip("") == "4":
        reset_jobfilters()
    elif choice.strip("") == "5":
        watchdog()
    else:
        menu()

def watchdog():
    "The main watchdog loop, break by using ctrl+c"

    _header()
    print("To break this loop, press ctrl+c")
    print(" ")

    # Get the jobs
    jobs = {}
    renjobs = deadline_utils.get_all_jobs("rendering")
    queuedjobs = deadline_utils.get_all_jobs("queued")
    jobs.update(queuedjobs)
    jobs.update(renjobs)

    # Get the jobfilters and format into a dict like:
    # {"FILTERNAME":[POOL, PRIORITY], "FILTERNAME2:[POOL, PRIORITY]"}
    # i.e. {"DD8": ["high", 100], "TD1": ["2d_main", 80]}
    jobfilters = {}
    for line in open(_get_jobfilters_file(), "r"):
        try:
            filtername = line.split(",")[0]
            pool = line.split(",")[1]
            priority = int(line.split(",")[2])
            jobfilters[filtername] = [pool, priority]
        except:
            pass

    for job_filter, settings in jobfilters.iteritems():
        job_filter = job_filter.strip(" ")

        #print job_filter
        #print settings
        #print " "

        for job_name, job_id in jobs.iteritems():
            #print job_name.lower()
            #print job_id
            if job_filter.lower() in job_name.lower():

                print("Updating job: {}".format(job_name))
                print(job_id)
                #print("Pool: {p}, Priority: {pr}".format(p=settings[0], pr=settings[1]))

                # set the job settings based on the job filter
                deadline_utils.set_job_setting([job_id], "Pool", settings[0])
                deadline_utils.set_job_setting([job_id], "Priority", str(settings[1]))


    print(" ")
    _dashingLine()
    print("Waiting 5 seconds...")
    time.sleep(5)
    watchdog()

    

    
        

def add_jobfilter():
    "Provides a menu for the user to add a jobfilter"
    _header()

    jobfilter = question("Enter a jobfilter to add:")
    print(" ")

    for pool in pools:
        print(pool)
    pool = question("Enter the pool any jobs matching this jobfilter should be reassigned to?\n(leave blank to leave it the same):")

    priority = question("What priority should any jobs matching the jobfilter be given?\n(leave blank to leave it the same):")

    # Add the jobfilters
    add_jobfilter_to_file(jobfilter, pool, priority)

    # Go back to the menu
    menu()  

def view_jobfilters():
    "Prints a list of the current jobfilters in the jobfilters file"
    _header()

    print("ID:  jobfilters:         Pool:       Priority:")
    _dashingLine()

    jobfilters_file = _get_jobfilters_file()
    f = open(jobfilters_file, "r")
    count = 1
    for line in f:
        formatted_line = line.split(",")
        print(str(count)+"    ".join(formatted_line))
        count = count+1
    f.close()
    print(" ")
    _dashingLine()
    print("Press enter to return to the main menu...")
    raw_input("")
    
    # Go back to the menu
    menu()  

def reset_jobfilters():
    "Resets the job filters"

    print("Removing jobfilters...")
    c = question("Are you sure? (y/n)")
    if c.strip("") == "y":
        jobfilters_file = _get_jobfilters_file()
        os.remove(jobfilters_file)
        _ensure_jobfilters_exist()

    # Go back to the menu
    menu()  


# Helper functions _
def _div():
    print(" ")
    _paddedLine()

def _paddedLine():
    print("###########################################")

def _dashingLine():
    print("-------------------------------------------")

def _header():
    os.system("cls")
    _div()
    print(app_name)
    print("Version: {}".format(version))
    _paddedLine()
    print(" ")

def _get_argv(argv):
    "Get's a argument from the command line args"
    args = sys.argv

    for arg in args:
        if argv in arg.lower():
            try:
                return arg.split("-"+argv+":")[1]
            except:
                return True
    return None

def _get_hostname():
    return socket.gethostname()

def _ensure_jobfilters_exist():
    jobfilters_file = _get_jobfilters_file()
    if not os.path.exists(jobfilters_file):
        f = open(jobfilters_file, "w")
        f.close()

def _get_jobfilters_file():
    return os.path.join(os.path.dirname(__file__), "jobfilters.cfg")

def add_jobfilter_to_file(jobfilter, pool, priority):
    "Add a line to the jobfilters file"
    jobfilters_file = _get_jobfilters_file()
    f = open(jobfilters_file, "a")
    f.write("\n {f},{p},{pr}".format(f=jobfilter, p=pool, pr=priority))
    f.close()
    print("Added jobfilter to jobfilters file...")

def question(question):
    print(" ")
    print(question)
    a = raw_input()
    return a

if __name__ == "__main__":
    main()