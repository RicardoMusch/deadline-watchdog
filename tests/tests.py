#import deadline_utils

# renjobs = deadline_utils.get_all_jobs("rendering")
# queuedjobs = deadline_utils.get_all_jobs("queued")
# jobs = {}
# jobs.update(queuedjobs)
# jobs.update(renjobs)
# print jobs

# jobs = renjobs
# jobs.update(queuedjobs)


# for jobname, jobid in jobs.iteritems():
#     print jobname
#     print jobid

#print deadline_utils.get_pools()

#deadline_utils.set_job_setting(["5fa03ee220b6ac1ab4703235"], "priority", "100")

#deadline_utils.get_all_jobs("rendering")


import ast

jobfilters_file = r"C:\Users\ricardom\Documents\github\deadline-watchdog\jobfilters.cfg"
f = open(jobfilters_file, "r")

for line in f:
    
    jobFilter = ast.literal_eval(line)
    for k, v in jobFilter.iteritems():
        print k
        print v