app_name = "Deadline Render Watchdog"
app_version = "v0.1"
time_to_sleep = 10

print "\n\n\n"
print "################################################"
print "    ", app_name, app_version
print "################################################"
print "\n"


import os
import subprocess
import time


def watchdog():
        
    jobs_to_prio = ["MAR_004A_0020"]


    "Get all Jobs with status Queued or Rendering"
    proc = subprocess.Popen([os.path.join(os.environ["DEADLINE_PATH"], "deadlinecommand.exe"), "getJobsFilterIni", "status=queued", "status=rendering"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    "Split output line by line into a list"
    out = out.split("\n")


    "Distill a list of ID and Jobname out of the output"
    jobs = []  
    for s in out:
        #print s
        if ("ID=" in s) or ("JobName=" in s):
            if not "JobDependencyIDs=" in s:
                if "ID" in s:
                    jobID = s
                    #print jobID
                    jobs.append(s)
                if "JobName=" in s:
                    jobName = s
                    jobs.append(s)
                    #print jobName


    "Create a dictionary with jobname as key and jobID as value"
    new_jobs_dict = {}    
    for s in jobs:
        #print s
        if "ID=" in s:
            jobID = s
            #print jobID
        if "JobName=" in s:
            jobName = s
            new_jobs_dict[jobName] = jobID


    "Print each job that Matches to the jobs_to_prio list"
    for k,v in new_jobs_dict.iteritems():
        for j in jobs_to_prio:
            if j.lower() in k.lower():
                print k
                print v


    time.sleep(time_to_sleep)
    watchdog()



"RUN APP"
watchdog()    


