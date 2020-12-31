import deadline_utils

# renjobs = deadline_utils.get_all_jobs("rendering")
# queuedjobs = deadline_utils.get_all_jobs("queued")

# jobs = renjobs
# jobs.update(queuedjobs)


# for jobname, jobid in jobs.iteritems():
#     print jobname
#     print jobid

print deadline_utils.get_pools()