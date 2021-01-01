import subprocess
import os
import sys
from random import randint
from subprocess import PIPE

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
            #print(name)
            #print(jobid)
            #print(" ")
            name = None
            jobid = None

    return jobs

def send_python_job(**kwargs):
    """
    Spawns a Python job on the current connected Deadline Repository.
    Returns the submission log.
    """

    print("Sending Job to Deadline...")
    
    ##############################################################
    #logger.debug("Writing Job Info File")
    ##############################################################
    jif = os.path.join(os.environ["TEMP"], str(randint(0,99999))+"_deadlineJobInfo.txt")
    #logger.debug(jif)
    file = open(jif,"w")
    file.write("Plugin=Python")

    if "Name" in kwargs.keys():
        file.write("\nName=" + kwargs["Name"])
    if "BatchName" in kwargs.keys():
        file.write("\nBatchName=" + kwargs["BatchName"])
    if "Department" in kwargs.keys():
        file.write("\nDepartment=" + kwargs["Department"])

    # Pool
    if "Pool" in kwargs.keys():
        file.write("\nPool=" + str(kwargs["Pool"]))

    # SecondaryPool
    if "SecondaryPool" in kwargs.keys():
        file.write("\nSecondaryPool=" + str(kwargs["SecondaryPool"]))

    # Machinelimit
    if "MachineLimit" in kwargs.keys():
        file.write("\nMachineLimit=" + str(kwargs["MachineLimit"]))

    # Limitgroups as list
    if "LimitGroups" in kwargs.keys():
        file.write("\nLimitGroups=" + ",".join(kwargs["LimitGroups"]))

    # Framerange - default 1
    if "Frames" in kwargs.keys():
        file.write("\nFrames=" + str(kwargs["Frames"]))
    else:
        file.write("\nFrames=1")

    # Chunksize - default 99999
    if "ChunkSize" in kwargs.keys():
        file.write("\nChunkSize=" + str(kwargs["ChunkSize"]))
    else:
        file.write("\nChunkSize=99999")

    # Priority - default 10
    if "Priority" in kwargs.keys():
        file.write("\nPriority=" + str(kwargs["Priority"]))
    else:
        file.write("\nPriority=10")

    # JobDependencies
    if "JobDependencies" in kwargs.keys():
        file.write("\nJobDependencies=" + ",".join(kwargs["JobDependencies"]))

    # OutputFiles
    if "OutputFiles" in kwargs.keys():
        count = 0
        for output_file in kwargs["OutputFiles"]:
            file.write("\nOutputFilename" + str(count) + "=" + output_file)
            count = count+1
    
    # InitialStatus
    if "InitialStatus" in kwargs.keys():
        file.write("\nInitialStatus=" + str(kwargs["InitialStatus"]))

    # EnvironmentKeyValues
    if "EnvironmentKeyValues" in kwargs.keys():
        count = 0
        for k, v in kwargs["EnvironmentKeyValues"].iteritems():
            file.write("\nEnvironmentKeyValue" + str(count) + "=" + k + "=" + str(v))
            count = count+1

    # Scripts
    if "PreJobScript" in kwargs.keys():
        script_path = str(kwargs["PreJobScript"]).replace("\\", "/")
        file.write("\nPreJobScript=" + script_path)
    if "PostJobScript" in kwargs.keys():
        script_path = str(kwargs["PostJobScript"]).replace("\\", "/")
        file.write("\nPostJobScript=" + script_path)
    if "PreTaskScript" in kwargs.keys():
        script_path = str(kwargs["PreTaskScript"]).replace("\\", "/")
        file.write("\nPreTaskScript=" + script_path)
    if "PostTaskScript" in kwargs.keys():
        script_path = str(kwargs["PostTaskScript"]).replace("\\", "/")
        file.write("\nPostTaskScript=" + script_path)

    # Close the file
    file.close()
   
    

    ##############################################################
    #logger.debug("Writing Plugin Info File")
    ##############################################################
    pif = os.path.join(os.environ["TEMP"], str(randint(0,99999))+"_deadlinePluginInfo.txt")
    #logger.debug(pif)
    file = open(pif,"w")
    file.write("Plugin=Python")

    # Arguments
    if "Arguments" in kwargs.keys():
        file.write("\nArguments=" + str(kwargs["Arguments"]))

    # SingleFramesOnly
    if "SingleFramesOnly" in kwargs.keys():
        file.write("\nSingleFramesOnly=" + str(kwargs["SingleFramesOnly"]))

    # Version
    if "Version" in kwargs.keys():
        file.write("\nVersion=" + str(kwargs["Version"]))
    else:
        # default to v2.7 if no version present
        file.write("\nVersion=2.7")

    # SceneFile
    if "ScriptFile" in kwargs.keys():
        file.write("\nScriptFile=" + str(kwargs["ScriptFile"]))

    # Close the file
    file.close()

    ##################################################
    #logger.debug("Sending Job to Farm")
    ##################################################
    deadlinecommand = os.path.join(os.environ["DEADLINE_PATH"], "deadlinecommand.exe")   
    proc = subprocess.Popen([deadlinecommand,jif,pif], stdout=PIPE, shell=True)
    output = proc.stdout.read()




