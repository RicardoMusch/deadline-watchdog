import subprocess
import os
import sys

def set_job_setting(jobs, settingname, value):
    "Sets the value of a setting for the job(s)."
    proc = subprocess.Popen([os.path.join(os.environ["DEADLINE_PATH"], "deadlinecommand.exe"), "setJobSetting", ",".join(jobs), settingname, value], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    print(out)

def get_pools():
    "Returns a list of pool names"
    proc = subprocess.Popen([os.path.join(os.environ["DEADLINE_PATH"], "deadlinecommand.exe"), "GetPoolNames", ], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    "Split output line by line into a list"
    out = out.split("\n")
    pools = []
    for pool in out:
        if not pool == "":
            pools.append(pool)
    return pools    

def get_all_jobs(status):
    "Get's queued jobs on the farm"

    # Get all Jobs with status Queued
    proc = subprocess.Popen([os.path.join(os.environ["DEADLINE_PATH"], "deadlinecommand.exe"), "getJobsFilterIni", "status={}".format(status),], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    "Split output line by line into a list"
    out = out.split("\n")
    #return out

    #name = (out.split("Name=")[1]).split("\n")[0]
    #print name

    jobs = {}
    name = None
    jobid = None
    for line in out:
        if "JobName=" in line:
            name = line.split("JobName=")[1]
            #print name
        if "ID=" in line:
            jobid = line.split("ID=")[1]
            #print jobid
        
        if name and jobid:
            jobs[name] = jobid

    return jobs

def get_all_jobs2(status):
    "Get's queued jobs on the farm"

    # Get all Jobs with status Queued
    proc = subprocess.Popen([os.path.join(os.environ["DEADLINE_PATH"], "deadlinecommand.exe"), "getJobsFilterIni", "status={}".format(status),], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    "Split output line by line into a list"
    
    # Split by empty line (each block between empty line is a job)
    out = out.split("\n ")

    # for block in out:
    #     print(block)

    # return

    
    
    #return out

    #name = (out.split("Name=")[1]).split("\n")[0]
    #print name

    jobs = {}
    for block in out:
        name = None
        jobid = None
        for line in block.split("\n"):
            if "JobName=" in line:
                name = line.split("JobName=")[1]
                #print name
            if "ID=" in line:
                jobid = line.split("ID=")[1]
                #print jobid
            
            if name and jobid:
                jobs[name] = jobid

                #print(name)
                #print(jobid)

        #print name
        #print jobid
    
    for k, v in jobs.iteritems():
        print k
        print v

    return jobs




