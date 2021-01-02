app_name = "Deadline Watchdog"
version = "dev"
time_to_wait = 30

import os
from os import system
import sys
import socket
import time
import ast

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "python"))
import deadline_utils

# Start app
os.system("cls")

## Load empty vars
pools = None


def main():
    "Main app run"
    _ensure_jobfilters_exist()

    if _get_argv("run"):
        watchdog()
    
    # GUI
    global version
    version = _get_app_version()
    
    print("Getting Deadline configuration...")
    global pools
    pools = deadline_utils.get_pools()

    menu()

def menu():
    "Menu with choices"

    _header()
    print("Choose your option:")
    _dashingLine()
    print("1 - Add jobfilter")
    print("2 - Remove jobfilter (Not implemented yet)")
    print("3 - View jobfilters")
    print("4 - Reset all jobfilters")
    print("5 - Send Deadline Watchdog Job to farm...")    
    print("9 - Start watchdog...")

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
        send_watchdog_job()
    elif choice.strip("") == "9":
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
    pendingjobs = deadline_utils.get_all_jobs("pending")
    jobs.update(queuedjobs)
    jobs.update(renjobs)
    jobs.update(pendingjobs)

    # Get the jobfilters from the jobfilters file
    for line in open(_get_jobfilters_file(), "r"):

        # Eval the line as it should be a dict
        jobFilter = ast.literal_eval(line)

        for job_name, job_id in jobs.iteritems():

            if jobFilter["jobfilter"].lower() in job_name.lower():

                print("Updating job: {} with ID: {}".format(job_name, job_id))

                # set the job settings based on the job filter
                for key in jobFilter.keys():
                    if not key == "jobfilter":
                        if not str(jobFilter[key]) == "":
                            deadline_utils.set_job_setting([job_id], key, jobFilter[key])

    print(" ")
    _dashingLine()
    print("Waiting {} seconds...".format(time_to_wait))
    time.sleep(time_to_wait)
    watchdog()  

def send_watchdog_job():
    "Sends a deadline python job which automatically starts watchdog"
    _header()
    kwargs = {}
    kwargs["Name"] = "Deadline Watchdog"
    kwargs["Arguments"] = "-run"
    kwargs["ScriptFile"] = __file__
    kwargs["InitialStatus"] = "Suspended"
    deadline_utils.send_python_job(**kwargs)    
    print(" ")
    _dashingLine()
    print("The job is suspended. Please edit the job parameters via Deadline Monitor.")
    question("Press Enter to return to the main menu.")
    menu()    

def add_jobfilter():
    "Provides a menu for the user to add a jobfilter"
    _header()

    jobFilter = {}

    jobFilter["jobfilter"] = question("New jobfilter:")
    
    print("Pools:")
    _dashingLine()
    for pool in pools:
        print(pool)
    jobFilter["pool"] = question("Enter the pool any jobs matching this jobfilter should be reassigned to?\n(leave blank to leave it the same):")

    jobFilter["priority"] = question("What priority should any jobs matching the jobfilter be given?\n(leave blank to leave it the same):")

    # Add the jobfilter
    add_jobfilter_to_file(jobFilter)

    # Go back to the menu
    menu()  

def remove_jobfilter():
    "Provides a menu for the user to add a jobfilter"
    _header()

    print("This functionality has not yet been added!")
    print("Returning to main menu in 5 seconds...")
    time.sleep(5)

    # Go back to the menu
    menu()  

def view_jobfilters():
    "Prints a list of the current jobfilters in the jobfilters file"
    _header()

    print("ID:  jobfilter:")
    _dashingLine()

    jobfilters_file = _get_jobfilters_file()
    f = open(jobfilters_file, "r")
    count = 1
    for line in f:
        formatted_line = line.split(",")
        print("{} {} {} {}".format(str(count).ljust(4), formatted_line[0].ljust(20), formatted_line[1].ljust(10), str(formatted_line[2]).ljust(10)))
        #print(str(count).ljust(4)+"    "+"    ".join(formatted_line))
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
    _header()

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
    system("TITLE {} {}".format(app_name, version))
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

def add_jobfilter_to_file(jobFilter):
    "Add a line to the jobfilters file"
    jobfilters_file = _get_jobfilters_file()
    f = open(jobfilters_file, "a")
    f.write("{}\n".format(str(jobFilter)))
    f.close()
    print("Added jobfilter to jobfilters file...")

def question(question):
    print(" ")
    print(question)
    a = raw_input()
    return a

def _get_app_version():
    "App is usually in a versioned folder"
    folder = os.path.basename(os.path.dirname(__file__))
    return folder



if __name__ == "__main__":
    main()